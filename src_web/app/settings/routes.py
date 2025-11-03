from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import settings_bp
from .forms import VKSettingsForm
from .. import db

@settings_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = VKSettingsForm()
    if form.validate_on_submit():
        current_user.vk_api_id = form.vk_api_id.data.strip()
        current_user.vk_group_id = form.vk_group_id.data.strip()
        db.session.commit()
        flash("Настройки VK сохранены.", "success")
        return redirect(url_for("settings.index"))
    # начальное заполнение из БД
    if not form.vk_api_id.data:
        form.vk_api_id.data = (current_user.vk_api_id or "")
    if not form.vk_group_id.data:
        form.vk_group_id.data = (current_user.vk_group_id or "")
    return render_template("settings/index.html", form=form)



