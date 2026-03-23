# routers/admin.py
from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from models import Mahsulot, Buyurtma, Xabar
from database import get_db
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL    = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY    = os.getenv("SUPABASE_KEY", "")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "rasmlar")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

ADMIN_LOGIN   = "admin"
ADMIN_PAROL   = "nastarin2026"
SESSIYA_KALIT = "nastarin_session"

def admin_tekshir(request: Request):
    return request.cookies.get(SESSIYA_KALIT) == "kirdi"

@router.get("/admin/login")
def login_sahifa(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request})

@router.post("/admin/login")
def login(request: Request, login: str = Form(...), parol: str = Form(...)):
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

    rasm_bytes = await rasm.read()
    rasm_nomi = rasm.filename
    
    supabase.storage.from_(SUPABASE_BUCKET).upload(
        path=rasm_nomi,
        file=rasm_bytes,
        file_options={"content-type": rasm.content_type}
    )

    rasm_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{rasm_nomi}"

    db.add(Mahsulot(nomi=nomi, narxi=narxi, tasviri=rasm_url))
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@router.get("/admin/mahsulot/ochir/{id}")
def mahsulot_ochir(request: Request, id: int, db: Session = Depends(get_db)):
    if not admin_tekshir(request):
        return RedirectResponse(url="/admin/login", status_code=303)

    mahsulot = db.query(Mahsulot).filter(Mahsulot.id == id).first()
    if mahsulot:
        rasm_nomi = mahsulot.tasviri.split("/")[-1]
        try:
            supabase.storage.from_(SUPABASE_BUCKET).remove([rasm_nomi])
        except:
            pass
        db.delete(mahsulot)
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@router.post("/admin/buyurtma/holat/{id}")
def buyurtma_holat(request: Request, id: int,
                   holat: str = Form(...),
                   db: Session = Depends(get_db)):
    if not admin_tekshir(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    buyurtma = db.query(Buyurtma).filter(Buyurtma.id == id).first()
    if buyurtma:
        setattr(buyurtma, "holat", holat)
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