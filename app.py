from flask import Flask, jsonify, request
import sqlite3
from datetime import date
from math import isfinite

app = Flask(__name__)

def get_db():
    connection = sqlite3.connect("games.db")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
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


USER_FIELDS = ["username", "email"]


def validate_user_fields(data, fields):
    for field in fields:
        if not isinstance(data[field], str) or not data[field].strip():
            return f"{field} must be a non-empty string"

    if "email" in fields and "@" not in data["email"]:
        return "email must be a valid email address"

    return None


def unique_field_error(error):
    for field in USER_FIELDS:
        if f"users.{field}" in str(error):
            return jsonify({"error": f"{field} is already taken"}), 409
    raise error


@app.post("/users")
def create_user():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be JSON"}), 400

    missing_fields = [field for field in USER_FIELDS if field not in data]
    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields,
        }), 400

    error = validate_user_fields(data, USER_FIELDS)
    if error:
        return jsonify({"error": error}), 400

    connection = get_db()
    try:
        cursor = connection.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            (data["username"].strip(), data["email"].strip()),
        )
        connection.commit()
        user = connection.execute(
            "SELECT * FROM users WHERE user_id = ?", (cursor.lastrowid,)
        ).fetchone()
    except sqlite3.IntegrityError as e:
        return unique_field_error(e)
    finally:
        connection.close()

    return jsonify(dict(user)), 201


@app.get("/users")
def list_users():
    connection = get_db()
    try:
        users = connection.execute("SELECT * FROM users ORDER BY user_id").fetchall()
    finally:
        connection.close()

    return jsonify([dict(user) for user in users])


@app.get("/users/<int:user_id>")
def get_user(user_id):
    connection = get_db()
    try:
        user = connection.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
    finally:
        connection.close()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(dict(user))


@app.patch("/users/<int:user_id>")
def update_user(user_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be JSON"}), 400

    fields = [field for field in USER_FIELDS if field in data]
    if not fields:
        return jsonify({
            "error": "Provide at least one field to update",
            "fields": USER_FIELDS,
        }), 400

    error = validate_user_fields(data, fields)
    if error:
        return jsonify({"error": error}), 400

    assignments = ", ".join(f"{field} = ?" for field in fields)
    values = [data[field].strip() for field in fields]

    connection = get_db()
    try:
        cursor = connection.execute(
            f"UPDATE users SET {assignments} WHERE user_id = ?",
            (*values, user_id),
        )
        connection.commit()
        user = connection.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
    except sqlite3.IntegrityError as e:
        return unique_field_error(e)
    finally:
        connection.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify(dict(user))


@app.delete("/users/<int:user_id>")
def delete_user(user_id):
    connection = get_db()
    try:
        cursor = connection.execute(
            "DELETE FROM users WHERE user_id = ?", (user_id,)
        )
        connection.commit()
    finally:
        connection.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "User not found"}), 404

    return "", 204
