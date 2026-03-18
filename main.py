#main.py
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from routers import katalog, orders, contact, admin

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(katalog.router)
app.include_router(orders.router)
app.include_router(contact.router)
app.include_router(admin.router)

templates = Jinja2Templates(directory="templates")

@app.get("/")
def bosh_sahifa(request: Request, db: Session = Depends(get_db)):
    from models import Mahsulot
    mahsulotlar = db.query(Mahsulot).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "mahsulotlar": mahsulotlar
    })