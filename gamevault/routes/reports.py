from flask import Blueprint, jsonify, request
from gamevault.auth import api_admin_required
from gamevault.db import get_db

reports_bp = Blueprint("reports", __name__)

GAMES_PER_TAG_SQL = """
SELECT t.tag_id, t.name, COUNT(gt.game_id) AS game_count
FROM tags t
JOIN game_tags gt ON gt.tag_id = t.tag_id
GROUP BY t.tag_id
ORDER BY game_count DESC, t.name
"""

MOST_OWNED_SQL = """
SELECT g.game_id, g.title, COUNT(l.user_id) AS owners
FROM games g
JOIN library l ON l.game_id = g.game_id
GROUP BY g.game_id
ORDER BY owners DESC, g.title
LIMIT 10
"""

PUBLISHERS_SQL = """
SELECT publisher, COUNT(*) AS game_count
FROM games
GROUP BY publisher
ORDER BY publisher COLLATE NOCASE
"""

PUBLISHER_OWNERS_SQL = """
SELECT u.user_id, u.username, COUNT(*) AS games_owned
FROM users u
JOIN library l ON l.user_id = u.user_id
JOIN games g ON g.game_id = l.game_id
WHERE g.publisher = ?
GROUP BY u.user_id
ORDER BY games_owned DESC, u.username
"""


def run(sql, params=()):
    connection = get_db()
    try:
        return [dict(row) for row in connection.execute(sql, params).fetchall()]
    finally:
        connection.close()


@reports_bp.get("/reports/games-per-tag")
@api_admin_required
def games_per_tag():
    return jsonify(run(GAMES_PER_TAG_SQL))


@reports_bp.get("/reports/most-owned")
@api_admin_required
def most_owned():
    return jsonify(run(MOST_OWNED_SQL))


@reports_bp.get("/reports/publishers")
@api_admin_required
def publishers():
    return jsonify(run(PUBLISHERS_SQL))


@reports_bp.get("/reports/publisher-owners")
@api_admin_required
def publisher_owners():
    publisher = request.args.get("publisher", "").strip()
    if not publisher:
        return jsonify({"error": "publisher query parameter is required"}), 400
    return jsonify(run(PUBLISHER_OWNERS_SQL, (publisher,)))
