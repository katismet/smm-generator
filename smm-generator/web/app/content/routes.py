from flask import render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from . import content_bp
from .forms import PostForm

# берём готовые генераторы и паблишер из предыдущего проекта
import sys
from pathlib import Path

# Добавляем путь к src модулям (работает локально и на PythonAnywhere)
# Локально: ищем smm_app, на сервере: модули в mysite/src/
base_path = Path(__file__).parent.parent.parent
smm_app_path = base_path.parent / "smm_app" / "src"
src_path = base_path / "src"

if str(src_path) not in sys.path and src_path.exists():
    sys.path.insert(0, str(src_path))
elif str(smm_app_path) not in sys.path and smm_app_path.exists():
    sys.path.insert(0, str(smm_app_path))

from src.generators.text_gen import PostGenerator
from src.generators.image_gen import ImageGenerator
from src.social_publishers.vk_publisher import VKPublisher

@content_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    preview = None
    image_url = None
    vk_link = None

    if form.validate_on_submit():
        # 0) Проверяем ключи для автопоста (для превью не требуются)
        if form.auto_post.data and not (current_user.vk_api_id and current_user.vk_group_id):
            flash("Для автопоста заполните Settings: VK API ID и VK Group ID.", "warning")
            form.auto_post.data = False  # отключим автопост, но превью покажем

        try:
            # 1) Генерация текста (всегда)
            post = PostGenerator().generate_post(
                topic=form.topic.data,
                tone=form.tone.data
            )
            preview = {
                "title": post.title,
                "text": post.text,
                "hashtags": " ".join(post.hashtags),
                "image_prompt": post.image_prompt,
            }

            # 2) Картинка (по галочке)
            img_path = None
            if form.generate_image.data:
                # сохраняем в static/uploads чтобы отдать через Flask
                src_web_dir = Path(__file__).parent.parent.parent
                out_dir = src_web_dir / "static" / "uploads"
                out_dir.mkdir(parents=True, exist_ok=True)
                image = ImageGenerator().generate_image(
                    prompt=post.image_prompt,
                    out_dir=str(out_dir),
                    size="1024x1024"
                )
                img_path = Path(image.path)
                image_url = f"/static/uploads/{img_path.name}"

            # 3) Автопост (по галочке)
            if form.auto_post.data:
                publisher = VKPublisher(
                    api_key=current_user.vk_api_id,
                    group_id=int(current_user.vk_group_id)
                )
                result = publisher.publish_post(
                    text=f"{post.title}\n\n{post.text}\n\n{' '.join(post.hashtags)}",
                    image_path=img_path if img_path else None
                )
                vk_link = f"https://vk.com/wall{result.full_id}"
                flash(f"Опубликовано во VK: {vk_link}", "success")

        except Exception as e:
            flash(f"Ошибка: {e}", "danger")

    return render_template(
        "content/create_post.html",
        form=form,
        user=current_user,
        preview=preview,
        image_url=image_url,
        vk_link=vk_link,
    )

