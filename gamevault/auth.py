from functools import wraps

from flask import (
    Blueprint, abort, g, jsonify, redirect, render_template, request, session, url_for,
)
from werkzeug.security import check_password_hash

from gamevault.db import get_db

auth_bp = Blueprint("auth", __name__)

USER_COLUMNS = "user_id, username, email, is_admin, steam_id, created_at"


def public_user(row):
    if row is None:
        return None
    user = dict(row)
    user["is_admin"] = bool(user["is_admin"])
    return user


@auth_bp.before_app_request
def load_current_user():
    g.user = None
    user_id = session.get("user_id")
    if user_id is None:
        return

    connection = get_db()
    try:
        g.user = public_user(connection.execute(
            f"SELECT {USER_COLUMNS} FROM users WHERE user_id = ?", (user_id,)
        ).fetchone())
    finally:
        connection.close()

    if g.user is None:
        session.clear()


@auth_bp.app_context_processor
def inject_current_user():
    return {"current_user": g.get("user")}


def can_manage(user_id):
    return g.user is not None and (g.user["is_admin"] or g.user["user_id"] == user_id)


def log_in(user_id):
    session.clear()
    session["user_id"] = user_id
    session.permanent = True


def api_login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if g.user is None:
            return jsonify({"error": "Log in first"}), 401
        return view(*args, **kwargs)
    return wrapper


def api_admin_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if g.user is None:
            return jsonify({"error": "Log in first"}), 401
        if not g.user["is_admin"]:
            return jsonify({"error": "Only admins can do that"}), 403
        return view(*args, **kwargs)
    return wrapper


def api_user_access_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if g.user is None:
            return jsonify({"error": "Log in first"}), 401
        if not can_manage(kwargs["user_id"]):
            return jsonify({"error": "You can only change your own account"}), 403
        return view(*args, **kwargs)
    return wrapper


def page_login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login_page", next=request.full_path.rstrip("?")))
        return view(*args, **kwargs)
    return wrapper


def page_admin_required(view):
    @wraps(view)
    @page_login_required
    def wrapper(*args, **kwargs):
        if not g.user["is_admin"]:
            abort(403)
        return view(*args, **kwargs)
    return wrapper


def page_user_access_required(view):
    @wraps(view)
    @page_login_required
    def wrapper(*args, **kwargs):
        if not can_manage(kwargs["user_id"]):
            abort(403)
        return view(*args, **kwargs)
    return wrapper


@auth_bp.get("/login")
def login_page():
    if g.user is not None:
        return redirect(url_for("pages.index"))
    return render_template("login.html")


@auth_bp.post("/api/login")
def login():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be JSON"}), 400

    login_name = data.get("username")
    password = data.get("password")
    if not isinstance(login_name, str) or not isinstance(password, str) or not login_name.strip():
        return jsonify({"error": "Enter your username and password"}), 400

    connection = get_db()
    try:
        row = connection.execute(
            f"SELECT {USER_COLUMNS}, password_hash FROM users WHERE username = ? OR email = ?",
            (login_name.strip(), login_name.strip()),
        ).fetchone()
    finally:
        connection.close()

    if row is None or not check_password_hash(row["password_hash"], password):
        return jsonify({"error": "Wrong username or password"}), 401

    log_in(row["user_id"])
    user = public_user(row)
    user.pop("password_hash")
    return jsonify(user)


@auth_bp.post("/api/logout")
def logout():
    session.clear()
    return "", 204


@auth_bp.get("/api/me")
def me():
    return jsonify(g.user)
