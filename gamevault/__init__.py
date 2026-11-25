from flask import Flask

from gamevault.db import init_db
from gamevault.routes.catalog import catalog_bp
from gamevault.routes.games import games_bp
from gamevault.routes.library import library_bp
from gamevault.routes.pages import pages_bp
from gamevault.routes.platforms import platforms_bp
from gamevault.routes.recommendations import recommendations_bp
from gamevault.routes.tags import tags_bp
from gamevault.routes.users import users_bp
from gamevault.routes.game_tags import game_tags_bp


def create_app():
    app = Flask(__name__)

    for blueprint in [games_bp, users_bp, library_bp, tags_bp, recommendations_bp, game_tags_bp, catalog_bp, platforms_bp]:
        app.register_blueprint(blueprint, url_prefix="/api")

    app.register_blueprint(pages_bp)
    app.cli.add_command(init_db)

    return app
