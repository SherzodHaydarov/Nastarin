# models.py
from database import Base
from sqlalchemy import Column, Integer, String, Float

class Mahsulot(Base):
    __tablename__ = "mahsulotlar"

    id      = Column(Integer, primary_key=True)
    nomi    = Column(String)
    narxi   = Column(Float)
    tasviri = Column(String)

class Buyurtma(Base):
    __tablename__ = "buyurtmalar"

    id          = Column(Integer, primary_key=True)
    ism         = Column(String)
    telefon     = Column(String)
    mahsulot_id = Column(Integer)
    izoh        = Column(String)
    holat       = Column(String, default="Yangi")

class Xabar(Base):
    __tablename__ = "xabarlar"

    id      = Column(Integer, primary_key=True)
    ism     = Column(String)
    telefon = Column(String)
    xabar   = Column(String)