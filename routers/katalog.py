# katalog.py
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models import Mahsulot
from database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/katalog")
def katalog(request: Request, db: Session = Depends(get_db)):
    mahsulotlar = db.query(Mahsulot).all()
    return templates.TemplateResponse("katalog.html", {
        "request": request,
        "mahsulotlar": mahsulotlar
    })
