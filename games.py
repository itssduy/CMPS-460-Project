from datetime import date
from math import isfinite

from flask import Blueprint, jsonify, request
from database import get_db

games_bp = Blueprint("games", __name__)

# Create a game
@games_bp.post("/games")
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

# List all games
@games_bp.get("/games")
def list_games():
    connection = get_db()
    try:
        data = connection.execute(
            """
            SELECT *
            FROM games
            """
        ).fetchall()
        connection.commit()
    finally:
        connection.close()

    return jsonify([dict(row) for row in data])

# Get specific game
@games_bp.get("/games/<int:game_id>")
def get_game(game_id):
    connection=get_db()
    try:
        data = connection.execute(
            """
            SELECT *
            FROM games
            WHERE game_id = ?
            """,
            (game_id,),
        ).fetchone()
        connection.commit()
    finally:
        connection.close()

    if data is None:
        return jsonify({"error": "Game not found"}), 404

    return jsonify(dict(data))

# Update games
@games_bp.patch("/games/<int:game_id>")
def update_game(game_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be in JSON"}), 400

    allowed_fields = {"title", "developer", "publisher", "release_date", "price"}
    unknown_fields = set(data) - allowed_fields

    if unknown_fields:
        return jsonify({
            "error": "Unknown fields",
            "fields": sorted(unknown_fields),
        }), 400

    if not any(value is not None for value in data.values()):
        return jsonify({"error": "Provide at least one non-null field to update"}), 400

    updates = {}

    for field in ["title", "developer", "publisher"]:
        value = data.get(field)
        if value is not None:
            if not isinstance(value, str) or not value.strip():
                return jsonify({"error": f"{field} must be a non-empty string"}), 400
            updates[field] = value.strip()

    release_date = data.get("release_date")
    if release_date is not None:
        if not isinstance(release_date, str) or not release_date.strip():
            return jsonify({"error": "release_date must be a non-empty string"}), 400
        try:
            date.fromisoformat(release_date)
        except ValueError:
            return jsonify({"error": "release_date must use YYYY-MM-DD format"}), 400
        updates["release_date"] = release_date

    price = data.get("price")
    if price is not None:
        if isinstance (price, bool) or not isinstance(price, (int, float)):
            return jsonify({"error": "price must be a numebr"}), 400
        if not isfinite(price) or price < 0:
            return jsonify({"error": "price must be a finite number of 0 or more"})
        updates["price"] = price

    connection = get_db()
    try:
        cursor = connection.execute(
            """
            UPDATE games
            SET title = COALESCE(?, title),
                developer = COALESCE(?, developer),
                publisher = COALESCE(?, publisher),
                release_date = COALESCE(?, release_date),
                price = COALESCE(?, price)
            WHERE game_id = ?
            """,
            (
                updates.get("title"),
                updates.get("developer"),
                updates.get("publisher"),
                updates.get("release_date"),
                updates.get("price"),
                game_id,
            )
        )
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Game not found"}), 404

        updated_game = connection.execute(
            "SELECT * FROM games WHERE game_id = ?",
            (game_id,),
        ).fetchone()
    finally:
        connection.close()

    return jsonify(dict(updated_game))

# Delete game
@games_bp.delete("/games/<int:game_id>")
def delete_game(game_id):
    connection = get_db()
    try:
        cursor=connection.execute(
            """
            DELETE FROM games
            WHERE game_id = ?
            """,
            (game_id,),
        )
        connection.commit()

        row_count = cursor.rowcount
    finally:
        connection.close()

    if row_count == 0:
        return jsonify({"error": "Game not found"}), 404

    return jsonify({"message": "Game successfully deleted"})
