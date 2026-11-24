from flask import Blueprint, jsonify, request
from gamevault.db import attach_platforms, get_db

library_bp = Blueprint("library", __name__)


def user_exists(connection, user_id):
    return connection.execute(
        "SELECT 1 FROM users WHERE user_id = ?", (user_id,)
    ).fetchone() is not None


@library_bp.get("/users/<int:user_id>/library")
def list_library(user_id):
    connection = get_db()
    try:
        if not user_exists(connection, user_id):
            return jsonify({"error": "User not found"}), 404

        games = connection.execute(
            """
            SELECT g.game_id, g.title, g.developer, g.publisher,
                   g.release_date, g.price, l.created_at AS added_at
            FROM library l
            JOIN games g ON g.game_id = l.game_id
            WHERE l.user_id = ?
            ORDER BY l.created_at DESC
            """,
            (user_id,),
        ).fetchall()
        games = attach_platforms(connection, games)
    finally:
        connection.close()

    return jsonify(games)


@library_bp.post("/users/<int:user_id>/library")
def add_to_library(user_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be JSON"}), 400

    game_id = data.get("game_id")
    if isinstance(game_id, bool) or not isinstance(game_id, int):
        return jsonify({"error": "game_id must be an integer"}), 400

    connection = get_db()
    try:
        if not user_exists(connection, user_id):
            return jsonify({"error": "User not found"}), 404

        game = connection.execute(
            "SELECT * FROM games WHERE game_id = ?", (game_id,)
        ).fetchone()
        if game is None:
            return jsonify({"error": "Game not found"}), 404

        owned = connection.execute(
            "SELECT 1 FROM library WHERE user_id = ? AND game_id = ?",
            (user_id, game_id),
        ).fetchone()
        if owned:
            return jsonify({"error": "Game is already in this user's library"}), 409

        connection.execute(
            "INSERT INTO library (user_id, game_id) VALUES (?, ?)",
            (user_id, game_id),
        )
        connection.commit()
    finally:
        connection.close()

    return jsonify(dict(game)), 201


@library_bp.delete("/users/<int:user_id>/library/<int:game_id>")
def remove_from_library(user_id, game_id):
    connection = get_db()
    try:
        cursor = connection.execute(
            "DELETE FROM library WHERE user_id = ? AND game_id = ?",
            (user_id, game_id),
        )
        connection.commit()
    finally:
        connection.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Game is not in this user's library"}), 404

    return "", 204
