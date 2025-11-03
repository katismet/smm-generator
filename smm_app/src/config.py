from dotenv import load_dotenv
import os

load_dotenv()

# OpenAI ключ - берется из .env или из настроек пользователя
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
# VK ключ и группа теперь хранятся у пользователя (Settings веб-приложения)
# и передаются из current_user через параметры функций
VK_API_KEY = os.getenv("VK_API_KEY", "")  # legacy: для CLI, в веб - из БД
VK_GROUP_ID = int(os.getenv("VK_GROUP_ID", "0"))  # legacy: для CLI, в веб - из БД

