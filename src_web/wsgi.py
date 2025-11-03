# WSGI файл для PythonAnywhere
# Этот файл должен быть загружен как WSGI конфигурация

import sys
import os

# Добавляем путь к проекту
path = '/home/TestZerocodSMM/mysite'
if path not in sys.path:
    sys.path.insert(0, path)

# Добавляем путь к src модулям (generators, social_publishers, etc.)
src_path = '/home/TestZerocodSMM/mysite/src'
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Импортируем приложение
from app import create_app

application = create_app()

