from flask import Blueprint, jsonify, request
from gamevault.db import attach_platforms, get_db

platforms_bp = Blueprint("platforms", __name__)


@platforms_bp.get("/platforms")
def list_platforms():
    connection = get_db()
    try:
        platforms = connection.execute(
            "SELECT * FROM platforms ORDER BY platform_id"
        ).fetchall()
    finally:
        connection.close()

    return jsonify([dict(platform) for platform in platforms])


@platforms_bp.put("/games/<int:game_id>/platforms")
def set_game_platforms(game_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be JSON"}), 400

    platform_ids = data.get("platform_ids")
    if not isinstance(platform_ids, list) or any(
        isinstance(value, bool) or not isinstance(value, int) for value in platform_ids
    ):
        return jsonify({"error": "platform_ids must be a list of integers"}), 400
    platform_ids = sorted(set(platform_ids))

    connection = get_db()
    try:
        game = connection.execute(
            "SELECT * FROM games WHERE game_id = ?", (game_id,)
        ).fetchone()
        if game is None:
            return jsonify({"error": "Game not found"}), 404

        if platform_ids:
            placeholders = ", ".join("?" for _ in platform_ids)
            found = connection.execute(
                f"SELECT COUNT(*) FROM platforms WHERE platform_id IN ({placeholders})",
                platform_ids,
            ).fetchone()[0]
            if found != len(platform_ids):
                return jsonify({"error": "One or more platforms do not exist"}), 400

        connection.execute("DELETE FROM game_platforms WHERE game_id = ?", (game_id,))
        connection.executemany(
            "INSERT INTO game_platforms (game_id, platform_id) VALUES (?, ?)",
            [(game_id, platform_id) for platform_id in platform_ids],
        )
        connection.commit()
        game = attach_platforms(connection, [game])[0]
    finally:
        connection.close()

    return jsonify(game)
