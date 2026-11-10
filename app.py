from flask import Flask, jsonify, request
import sqlite3
from datetime import date
from math import isfinite

app = Flask(__name__)

def get_db():
    connection = sqlite3.connect("games.db")
    connection.row_factory = sqlite3.Row
    return connection

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.post("/games")
def create_game():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be JSON"}), 400

    required_fields = [
        "title",
        "developer",
        "publisher",
        "release_date",
        "price",
    ]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify ({
            "error": "Missing required fields",
            "fields": missing_fields,
        }), 400

    for field in ["title", "developer", "publisher", "release_date"]:
        if not isinstance(data[field], str) or not data[field].strip():
            return jsonify({"error": f"{field} must be a non-empty string"}), 400

    try:
        date.fromisoformat(data["release_date"])
    except ValueError:
        return jsonify({"error": "release_date must use YYYY-MM-DD format"}), 400

    price = data["price"]
    if isinstance(price, bool) or not isinstance(price, (int, float)):
        return jsonify({"error": "price must be a number"}), 400

    if not isfinite(price) or price < 0:
        return jsonify({"error": "price must be a finite number of 0 or more"}), 400

    connection = get_db()
    try:
        cursor = connection.execute(
            """
            INSERT INTO games (title, developer, publisher, release_date, price)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                data["title"].strip(),
                data["developer"].strip(),
                data["publisher"].strip(),
                data["release_date"],
                price,
            ),
        )
        connection.commit()
        game_id = cursor.lastrowid
    finally:
        connection.close()

    return jsonify({
        "game_id": game_id,
        "title": data["title"].strip(),
        "developer": data["developer"].strip(),
        "publisher": data["publisher"].strip(),
        "release_date": data["release_date"],
        "price": price,
    }), 201