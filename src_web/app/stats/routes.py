from __future__ import annotations
from flask import render_template, flash
from flask_login import login_required, current_user

from . import stats_bp

# Импортируем функции из smm_app
import sys
from pathlib import Path

# Работает локально и на PythonAnywhere
base_path = Path(__file__).parent.parent.parent
smm_app_path = base_path.parent / "smm_app" / "src"
src_path = base_path / "src"

if str(src_path) not in sys.path and src_path.exists():
    sys.path.insert(0, str(src_path))
elif str(smm_app_path) not in sys.path and smm_app_path.exists():
    sys.path.insert(0, str(smm_app_path))

from src.social_stats.vk_stats import get_summary


@stats_bp.route("/")
@login_required
def index():
    if not (current_user.vk_api_id and current_user.vk_group_id):
        flash("Сначала в Settings введите VK API ID и VK Group ID.", "warning")
        return render_template("stats/index.html", summary=None)
    
    try:
        # Временно заменяем токен в модуле для получения статистики
        import src.social_stats.vk_stats as vk_module
        original_token = vk_module.VK_API_KEY
        original_group = vk_module.VK_GROUP_ID
        
        vk_module.VK_API_KEY = current_user.vk_api_id
        vk_module.VK_GROUP_ID = int(current_user.vk_group_id)
        
        try:
            summary = get_summary(int(current_user.vk_group_id), last_n=10)
        finally:
            # Восстанавливаем оригинальные значения
            vk_module.VK_API_KEY = original_token
            vk_module.VK_GROUP_ID = original_group
            
        return render_template("stats/index.html", summary=summary)
    except Exception as e:
        flash(f"Ошибка получения статистики: {e}", "danger")
        return render_template("stats/index.html", summary=None)

