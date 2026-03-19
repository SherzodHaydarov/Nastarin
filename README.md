# Nastarin
 
## Ishga tushirish

python -m venv venv             -->  # Terminalda venv vertual muhit sozlanadi

pip freeze > requirements.txt   -->  # Frameworklar ro'yxatini yuklab oling 

python add_test_data.py         -->  # Sahifaga joylangan suratlarning barchasini yuklash

python delete_data.py           -->  # Sahifaga joylangan suratlarning barchasini o'chirish

uvicorn main:app --reload       -->  # bu komanda bilan loyiha ishga tushadi. http://127.0.0.1:8000 ni Ctrl + sichqonchaning chap tugmasi bosilsa, server ishga tushadi.
