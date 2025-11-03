# 📦 Точный список файлов для PythonAnywhere

## ✅ НУЖНО ЗАГРУЗИТЬ:

### Структура на сервере: `/home/TestZerocodSMM/mysite/`

```
mysite/
├── app/                    ← Из src_web/app/ (ВСЯ ПАПКА)
│   ├── __init__.py
│   ├── models.py
│   ├── auth/
│   ├── content/
│   ├── settings/
│   └── stats/
│
├── templates/              ← Из src_web/templates/ (ВСЯ ПАПКА)
│   ├── base.html
│   ├── auth/
│   ├── content/
│   ├── settings/
│   └── stats/
│
├── static/                 ← Из src_web/static/ (ВСЯ ПАПКА)
│   └── uploads/            (пустая папка, создастся автоматически)
│
├── src/                    ← Из smm_app/src/ (МОДУЛИ, НЕ ВСЯ ПАПКА!)
│   ├── __init__.py         ← Из smm_app/src/__init__.py
│   ├── config.py           ← Из smm_app/src/config.py ⚠️ ВАЖНО!
│   ├── generators/         ← Из smm_app/src/generators/ (вся папка)
│   ├── social_publishers/  ← Из smm_app/src/social_publishers/ (вся папка)
│   ├── social_stats/       ← Из smm_app/src/social_stats/ (вся папка)
│   └── utils/              ← Из smm_app/src/utils/ (вся папка)
│
├── requirements.txt        ← Из src_web/requirements.txt
└── wsgi.py                 ← Из src_web/wsgi.py ⚠️ ТОЧКА ВХОДА!
```

## ❌ НЕ ЗАГРУЖАТЬ:

- ❌ `src_web/main.py` - НЕ нужен (используется wsgi.py)
- ❌ `smm_app/src/main.py` - НЕ нужен (это CLI версия)
- ❌ `__pycache__/` - создастся автоматически
- ❌ `.venv/` - создастся на сервере
- ❌ `instance/site.db` - создастся автоматически
- ❌ `smm_app/src/smm_app.egg-info/` - не нужен

## 📋 Чек-лист:

- [ ] Загрузить `src_web/app/` → `mysite/app/`
- [ ] Загрузить `src_web/templates/` → `mysite/templates/`
- [ ] Загрузить `src_web/static/` → `mysite/static/`
- [ ] Загрузить `smm_app/src/config.py` → `mysite/src/config.py` ⚠️
- [ ] Загрузить `smm_app/src/__init__.py` → `mysite/src/__init__.py`
- [ ] Загрузить `smm_app/src/generators/` → `mysite/src/generators/`
- [ ] Загрузить `smm_app/src/social_publishers/` → `mysite/src/social_publishers/`
- [ ] Загрузить `smm_app/src/social_stats/` → `mysite/src/social_stats/`
- [ ] Загрузить `smm_app/src/utils/` → `mysite/src/utils/`
- [ ] Загрузить `src_web/requirements.txt` → `mysite/requirements.txt`
- [ ] Загрузить `src_web/wsgi.py` → `mysite/wsgi.py` ⚠️ ГЛАВНЫЙ ФАЙЛ!

## 🔑 Важно:

1. **wsgi.py** - это главный файл для запуска (аналог main.py для сервера)
2. **config.py** - обязательно нужен, содержит настройки загрузки .env
3. **Все папки со всеми файлами внутри** - включая `__init__.py`



