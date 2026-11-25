from flask import Blueprint, render_template

from gamevault.auth import page_admin_required, page_user_access_required
from gamevault.routes import reports as report_queries

pages_bp = Blueprint("pages", __name__)


@pages_bp.get("/")
def index():
    return render_template("index.html")


@pages_bp.get("/users")
@page_admin_required
def users():
    return render_template("users/list.html")


@pages_bp.get("/users/new")
def new_user():
    return render_template("users/new.html")


@pages_bp.get("/users/<int:user_id>")
@page_user_access_required
def user_profile(user_id):
    return render_template("users/profile.html", user_id=user_id)


@pages_bp.get("/users/<int:user_id>/library")
def user_library(user_id):
    return render_template("users/library.html", user_id=user_id)


@pages_bp.get("/games/<int:game_id>")
def game_detail(game_id):
    return render_template("games/detail.html", game_id=game_id)


@pages_bp.get("/games/new")
@page_admin_required
def new_game():
    return render_template("games/form.html", game_id=None)


@pages_bp.get("/games/<int:game_id>/edit")
@page_admin_required
def edit_game(game_id):
    return render_template("games/form.html", game_id=game_id)


@pages_bp.get("/reports")
@page_admin_required
def reports():
    return render_template("reports.html", sql=report_queries)


@pages_bp.get("/players")
def players():
    return render_template("players.html")


@pages_bp.get("/tags")
@page_admin_required
def tags():
    return render_template("tags.html")
