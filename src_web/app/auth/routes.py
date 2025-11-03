from __future__ import annotations
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from . import auth_bp
from .forms import RegisterForm, LoginForm
from .. import db
from ..models import User

@auth_bp.route("/")
def auth_index():
    from flask import redirect, url_for
    return redirect(url_for("auth.login"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter((User.email == form.email.data) | (User.username == form.username.data)).first():
            flash("Пользователь с таким email/именем уже существует", "warning")
            return render_template("auth/register.html", form=form)

        user = User(username=form.username.data.strip(), email=form.email.data.strip().lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("auth.dashboard"))
    return render_template("auth/register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.strip()).first()
        if not user or not user.check_password(form.password.data):
            flash("Неверное имя пользователя или пароль", "danger")
            return render_template("auth/login.html", form=form)
        login_user(user, remember=True)
        next_page = request.args.get("next")
        return redirect(next_page or url_for("auth.dashboard"))
    return render_template("auth/login.html", form=form)

@auth_bp.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth_bp.get("/dashboard")
@login_required
def dashboard():
    return render_template("auth/dashboard.html", user=current_user)

