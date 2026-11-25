from flask import Blueprint, jsonify
from gamevault.db import get_db

players_bp = Blueprint("players", __name__)

PLAYER_SELECT = """
    SELECT u.user_id, u.username, u.created_at,
           (SELECT COUNT(*) FROM library l WHERE l.user_id = u.user_id) AS game_count
    FROM users u
"""


@players_bp.get("/players")
def list_players():
    connection = get_db()
    try:
        players = connection.execute(
            f"{PLAYER_SELECT} WHERE u.is_admin = 0 ORDER BY game_count DESC, u.username COLLATE NOCASE"
        ).fetchall()
    finally:
        connection.close()

    return jsonify([dict(player) for player in players])


@players_bp.get("/players/<int:user_id>")
def get_player(user_id):
    connection = get_db()
    try:
        player = connection.execute(
            f"{PLAYER_SELECT} WHERE u.user_id = ?", (user_id,)
        ).fetchone()
    finally:
        connection.close()

    if player is None:
        return jsonify({"error": "Player not found"}), 404

    return jsonify(dict(player))


@players_bp.get("/games/<int:game_id>/owners")
def list_owners(game_id):
    connection = get_db()
    try:
        owners = connection.execute(
            """
            SELECT u.user_id, u.username
            FROM library l
            JOIN users u ON u.user_id = l.user_id
            WHERE l.game_id = ?
            ORDER BY l.created_at
            """,
            (game_id,),
        ).fetchall()
    finally:
        connection.close()

    return jsonify([dict(owner) for owner in owners])
