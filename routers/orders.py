# routers/orders.py
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional
from models import Buyurtma, Mahsulot
from database import get_db
from notify import telegram_yuborish, email_yuborish

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/buyurtma")
def buyurtma_sahifa(request: Request, mahsulot: Optional[int] = None, db: Session = Depends(get_db)):
    mahsulotlar = db.query(Mahsulot).all()
    return templates.TemplateResponse("order.html", {
        "request": request,
        "mahsulotlar": mahsulotlar,
        "tanlangan": mahsulot
    })

@router.post("/buyurtma")
def buyurtma_yuborish(
    ism: str = Form(...),
    telefon: str = Form(...),
    mahsulot_id: int = Form(...),
    izoh: str = Form(""),
    db: Session = Depends(get_db)
):
    if not telefon.startswith("+998") or len(telefon) != 13:
        return RedirectResponse(url="/buyurtma?xato=1", status_code=303)

    yangi = Buyurtma(ism=ism, telefon=telefon, mahsulot_id=mahsulot_id, izoh=izoh)
    db.add(yangi)
    db.commit()

    telegram_matn = (
        f"🛍️ YANGI BUYURTMA!\n"
        f"{'─' * 25}\n"
        f"👤 Ism: {ism}\n"
        f"📞 Telefon: {telefon}\n"
        f"🎀 Mahsulot ID: {mahsulot_id}\n"
        f"💬 Izoh: {izoh or 'Yo`q'}\n"
        f"{'─' * 25}\n"
        f"⏰ Nastarin Pardalar"
    )

    email_matn = f"""
Hurmatli admin,

Yangi buyurtma kelib tushdi!

Mijoz ismi: {ism}
Telefon: {telefon}
Mahsulot ID: {mahsulot_id}
Izoh: {izoh or "Yo'q"}

Buyurtmani admin panelda ko'rish uchun:
https://nastarin.up.railway.app/admin

Hurmat bilan,
Nastarin Pardalar tizimi
    """

    try:
        telegram_yuborish(telegram_matn)
    except Exception as e:
        print(f"Telegram xato: {e}")

    try:
        email_yuborish("🛍️ Yangi buyurtma — Nastarin", email_matn)
    except Exception as e:
        print(f"Email xato: {e}")

    return RedirectResponse(url="/buyurtma?muvaffaqiyat=1", status_code=303)