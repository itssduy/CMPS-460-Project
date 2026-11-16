from flask import Flask

from gamevault.db import init_db
from gamevault.routes.games import games_bp
from gamevault.routes.library import library_bp
from gamevault.routes.users import users_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(games_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(library_bp)
    app.cli.add_command(init_db)

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    return app
