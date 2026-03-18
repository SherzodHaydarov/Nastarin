# delete_data.py
from database import SessionLocal
from models import Mahsulot

db = SessionLocal()
db.query(Mahsulot).delete()
db.commit()
db.close()

print("Barcha mahsulotlar o'chirildi!")