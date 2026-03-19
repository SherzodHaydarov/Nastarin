# add_test_data.py
from database import SessionLocal
from models import Mahsulot

db = SessionLocal()

mahsulotlar = [
    Mahsulot(nomi="Elita parda", narxi=3000000, tasviri="parda1.jpg"),
    Mahsulot(nomi="Eshik uchun parda", narxi=2500000, tasviri="parda2.jpg"),
    Mahsulot(nomi="Tulle oq parda", narxi=3000000, tasviri="parda3.jpg"),
]

db.add_all(mahsulotlar)
db.commit()
db.close()

print("Mahsulotlar qo'shildi!")