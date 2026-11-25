import os

from flask import Flask, jsonify

from gamevault.auth import auth_bp
from gamevault.db import init_db
from gamevault.routes.catalog import catalog_bp
from gamevault.routes.games import games_bp
from gamevault.routes.images import images_bp
from gamevault.routes.library import library_bp
from gamevault.routes.pages import pages_bp
from gamevault.routes.platforms import platforms_bp
from gamevault.routes.recommendations import recommendations_bp
from gamevault.routes.steam import steam_bp
from gamevault.routes.tags import tags_bp
from gamevault.routes.users import users_bp
from gamevault.routes.game_tags import game_tags_bp


def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
    app.config["STEAM_API_KEY"] = os.environ.get("STEAM_API_KEY")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or os.urandom(32)
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    for blueprint in [games_bp, users_bp, library_bp, tags_bp, recommendations_bp, game_tags_bp, catalog_bp, platforms_bp, images_bp]:
        app.register_blueprint(blueprint, url_prefix="/api")

    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(steam_bp)
    app.cli.add_command(init_db)

    @app.errorhandler(413)
    def file_too_large(error):
        return jsonify({"error": "Image must be 5 MB or smaller"}), 413

    return app
