# notify.py
import httpx
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN   = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
EMAIL_FROM       = os.getenv("EMAIL_FROM", "")
EMAIL_PASSWORD   = os.getenv("EMAIL_PASSWORD", "")
EMAIL_TO         = os.getenv("EMAIL_TO", "")

def telegram_yuborish(matn: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    httpx.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": matn})

def email_yuborish(mavzu: str, matn: str):
    msg = MIMEText(matn, "plain", "utf-8")
    msg["Subject"] = str(mavzu)
    msg["From"]    = str(EMAIL_FROM)
    msg["To"]      = str(EMAIL_TO)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(str(EMAIL_FROM), str(EMAIL_PASSWORD))
        server.send_message(msg)