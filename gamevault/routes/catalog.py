from flask import Blueprint, jsonify, request
from gamevault.db import attach_platforms, attach_tags, get_db

catalog_bp = Blueprint("catalog", __name__)

SORTS = {
    "title": "g.title COLLATE NOCASE",
    "price": "g.price ASC, g.title COLLATE NOCASE",
    "newest": "g.release_date DESC, g.title COLLATE NOCASE",
    "oldest": "g.release_date ASC, g.title COLLATE NOCASE",
    "popular": "popularity DESC, g.title COLLATE NOCASE",
}

GAME_SELECT = """
    SELECT g.*,
           (SELECT COUNT(*) FROM library l WHERE l.game_id = g.game_id) AS popularity
    FROM games g
"""


@catalog_bp.get("/catalog")
def list_catalog():
    sort = request.args.get("sort", "title")
    if sort not in SORTS:
        return jsonify({"error": "sort must be one of: " + ", ".join(SORTS)}), 400

    conditions = []
    params = []

    search = request.args.get("q", "").strip()
    if search:
        conditions.append("g.title LIKE ?")
        params.append(f"%{search}%")

    publisher = request.args.get("publisher", "").strip()
    if publisher:
        conditions.append("g.publisher = ? COLLATE NOCASE")
        params.append(publisher)

    tag = request.args.get("tag", "").strip()
    if tag:
        conditions.append("""
            EXISTS (
                SELECT 1 FROM game_tags gt
                JOIN tags t ON t.tag_id = gt.tag_id
                WHERE gt.game_id = g.game_id AND t.name = ? COLLATE NOCASE
            )
        """)
        params.append(tag)

    platform = request.args.get("platform", "").strip()
    if platform:
        conditions.append("""
            EXISTS (
                SELECT 1 FROM game_platforms gp
                JOIN platforms p ON p.platform_id = gp.platform_id
                WHERE gp.game_id = g.game_id AND p.name = ? COLLATE NOCASE
            )
        """)
        params.append(platform)

    where = "WHERE " + " AND ".join(conditions) if conditions else ""

    connection = get_db()
    try:
        games = connection.execute(
            f"{GAME_SELECT} {where} ORDER BY {SORTS[sort]}", params
        ).fetchall()
        games = attach_tags(connection, attach_platforms(connection, games))
    finally:
        connection.close()

    return jsonify(games)


@catalog_bp.get("/catalog/<int:game_id>")
def get_catalog_game(game_id):
    connection = get_db()
    try:
        game = connection.execute(
            f"{GAME_SELECT} WHERE g.game_id = ?", (game_id,)
        ).fetchone()
        if game is None:
            return jsonify({"error": "Game not found"}), 404
        game = attach_tags(connection, attach_platforms(connection, [game]))[0]
    finally:
        connection.close()

    return jsonify(game)
