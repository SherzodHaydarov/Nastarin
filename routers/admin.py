# routers/admin.py
from fastapi import APIRouter, Request, Depends, Form, UploadFile, File, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session
from models import Mahsulot, Buyurtma, Xabar
from database import get_db
import shutil
import os
import secrets

router = APIRouter()
templates = Jinja2Templates(directory="templates")

ADMIN_LOGIN    = "admin"
ADMIN_PAROL    = "Volidam@"
SESSIYA_KALIT  = "nastarin_session"

def admin_tekshir(request: Request):
    return request.cookies.get(SESSIYA_KALIT) == "kirdi"

@router.get("/admin/login")
def login_sahifa(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request})

@router.post("/admin/login")
def login(request: Request, response: Response,
          login: str = Form(...), parol: str = Form(...)):
    if login == ADMIN_LOGIN and parol == ADMIN_PAROL:
        resp = RedirectResponse(url="/admin", status_code=303)
        resp.set_cookie(SESSIYA_KALIT, "kirdi")
        return resp
    return templates.TemplateResponse("admin/login.html", {
        "request": request,
        "xato": "Login yoki parol noto'g'ri!"
    })

@router.get("/admin/logout")
def logout():
    resp = RedirectResponse(url="/admin/login", status_code=303)
    resp.delete_cookie(SESSIYA_KALIT)
    return resp

@router.get("/admin")
def dashboard(request: Request, db: Session = Depends(get_db)):
    if not admin_tekshir(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "mahsulotlar": db.query(Mahsulot).all(),
        "buyurtmalar": db.query(Buyurtma).all(),
        "xabarlar": db.query(Xabar).all(),
    })

@router.post("/admin/mahsulot/qosh")
async def mahsulot_qosh(
    request: Request,
    nomi: str = Form(...),
    narxi: float = Form(...),
    rasm: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not admin_tekshir(request):
        return RedirectResponse(url="/admin/login", status_code=303)

    rasm_nomi = rasm.filename
    with open(f"static/images/{rasm_nomi}", "wb") as f:
        shutil.copyfileobj(rasm.file, f)

    db.add(Mahsulot(nomi=nomi, narxi=narxi, tasviri=rasm_nomi))
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@router.get("/admin/mahsulot/ochir/{id}")
def mahsulot_ochir(request: Request, id: int, db: Session = Depends(get_db)):
    if not admin_tekshir(request):
        return RedirectResponse(url="/admin/login", status_code=303)

    mahsulot = db.query(Mahsulot).filter(Mahsulot.id == id).first()
    if mahsulot:
        rasm_yoli = f"static/images/{mahsulot.tasviri}"
        if os.path.exists(rasm_yoli):
            os.remove(rasm_yoli)
        db.delete(mahsulot)
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@router.get("/admin/buyurtma/ochir/{id}")
def buyurtma_ochir(request: Request, id: int, db: Session = Depends(get_db)):
    if not admin_tekshir(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    db.query(Buyurtma).filter(Buyurtma.id == id).delete()
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@router.get("/admin/xabar/ochir/{id}")
def xabar_ochir(request: Request, id: int, db: Session = Depends(get_db)):
    if not admin_tekshir(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    db.query(Xabar).filter(Xabar.id == id).delete()
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)