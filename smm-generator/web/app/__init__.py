from __future__ import annotations
import os
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    # Определяем путь к папке src_web
    src_web_dir = Path(__file__).parent.parent
    templates_dir = src_web_dir / "templates"
    
    app = Flask(__name__, template_folder=str(templates_dir))
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///site.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # csrf в Flask-WTF включён по SECRET_KEY

    db.init_app(app)
    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"   # куда редиректить неавторизованных
    login_manager.login_message = "Пожалуйста, войдите в аккаунт."
    login_manager.session_protection = "strong"

    from . import models  # noqa
    with app.app_context():
        db.create_all()

    # blueprints
    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    
    from .content.routes import content_bp
    app.register_blueprint(content_bp, url_prefix="/content")
    
    from .settings.routes import settings_bp
    app.register_blueprint(settings_bp, url_prefix="/settings")
    
    from .stats.routes import stats_bp
    app.register_blueprint(stats_bp, url_prefix="/stats")

    @app.get("/")
    def index():
        from flask import redirect, url_for
        from flask_login import current_user
        if getattr(current_user, "is_authenticated", False):
            return redirect(url_for("settings.index"))
        return "SMM Assistant (Flask) — OK. Зайдите на /auth/login или /auth/register"

    return app

