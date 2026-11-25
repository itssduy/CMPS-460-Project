from flask import Blueprint, jsonify, request
from gamevault.db import attach_platforms, get_db

recommendations_bp = Blueprint("recommendations", __name__)


@recommendations_bp.get("/users/<int:user_id>/recommendations")
def recommend_games(user_id):
    limit = request.args.get("limit", 10, type=int)
    if limit < 1 or limit > 50:
        return jsonify({"error": "limit must be between 1 and 50"}), 400

    connection = get_db()
    try:
        user = connection.execute(
            "SELECT 1 FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        if user is None:
            return jsonify({"error": "User not found"}), 404

        games = connection.execute(
            """
            WITH owned AS (
                SELECT game_id FROM library WHERE user_id = ?
            ),
            owned_tags AS (
                SELECT DISTINCT gt.tag_id
                FROM game_tags gt
                JOIN owned o ON o.game_id = gt.game_id
            )
            SELECT g.game_id, g.title, g.developer, g.publisher,
                   g.release_date, g.price, g.image_url,
                   COUNT(*) AS shared_tag_count,
                   GROUP_CONCAT(t.name, '|') AS shared_tags
            FROM games g
            JOIN game_tags gt ON gt.game_id = g.game_id
            JOIN owned_tags ot ON ot.tag_id = gt.tag_id
            JOIN tags t ON t.tag_id = gt.tag_id
            WHERE g.game_id NOT IN (SELECT game_id FROM owned)
              AND t.name <> 'Discount'
            GROUP BY g.game_id
            ORDER BY shared_tag_count DESC, g.title
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
        games = attach_platforms(connection, games)
    finally:
        connection.close()

    for game in games:
        game["shared_tags"] = sorted(game["shared_tags"].split("|"))

    return jsonify(games)
