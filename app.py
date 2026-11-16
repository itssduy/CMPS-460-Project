from flask import Flask
from games import games_bp
from users import users_bp

app = Flask(__name__)
app.register_blueprint(games_bp)
app.register_blueprint(users_bp)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
