# routers/contact.py
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from models import Xabar
from database import get_db
from notify import telegram_yuborish, email_yuborish

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/aloqa")
def aloqa_sahifa(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@router.post("/aloqa")
def xabar_yuborish(
    ism: str = Form(...),
    telefon: str = Form(...),
    xabar: str = Form(...),
    db: Session = Depends(get_db)
):
    yangi = Xabar(ism=ism, telefon=telefon, xabar=xabar)
    db.add(yangi)
    db.commit()

    telegram_matn = (
        f"💬 YANGI XABAR!\n"
        f"{'─' * 25}\n"
        f"👤 Ism: {ism}\n"
        f"📞 Telefon: {telefon}\n"
        f"💬 Xabar: {xabar}\n"
        f"{'─' * 25}\n"
        f"⏰ Nastarin Pardalar"
    )

    email_matn = f"""
Hurmatli admin,

Yangi xabar kelib tushdi!

Mijoz ismi : {ism}
Telefon : {telefon}
Xabar : {xabar}

Xabarni admin panelda ko'rish uchun:
http://127.0.0.1:8000/admin

Hurmat bilan,
Nastarin Pardalar tizimi
    """

    try:
        telegram_yuborish(telegram_matn)
    except Exception as e:
        print(f"Telegram xato: {e}")

    try:
        email_yuborish("💬 Yangi xabar — Nastarin", email_matn)
    except Exception as e:
        print(f"Email xato: {e}")

    return RedirectResponse(url="/aloqa?muvaffaqiyat=1", status_code=303)
