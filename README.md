# Nastarin Pardalar

Qarshi tumandagi pardalar tikish tsexining veb sayti.

## Ishga tushirish

### 1. Virtual muhit yaratish
```bash
python -m venv venv
```

### 2. Virtual muhitni yoqish
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. Loyihani ishga tushirish
```bash
uvicorn main:app --reload
```

Brauzerda oching: http://127.0.0.1:8000

---

### Qo'shimcha komandalar

Test ma'lumotlar qo'shish:
```bash
python add_test_data.py
```

Barcha ma'lumotlarni o'chirish:
```bash
python delete_data.py
```

## Texnologiyalar

- FastAPI
- SQLAlchemy
- Jinja2
- SQLite