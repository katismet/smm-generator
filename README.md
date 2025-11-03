# SMM Generator

Две части:
1) smm_app — CLI-генератор текстов и промтов изображения.
2) src_web — веб-версия (Flask) для деплоя.

## CLI (smm_app)
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
python src/app.py --topic "фитнес утром" --tone "спокойный" --length short --platform instagram

## Web (src_web)
python -m venv .venv
.venv\Scripts\activate
pip install -r src_web/requirements.txt
set FLASK_APP=src_web/main.py
flask run
