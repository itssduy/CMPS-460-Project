import sqlite3

from flask import Blueprint, jsonify, request
from gamevault.db import get_db

game_tags_bp = Blueprint("game_tags", __name__)

# Attatch a tag to a game
@game_tags_bp.post("/games/<int:game_id>/tags")
def add_game_tag(game_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be JSON"}), 400

    tag_id = data.get("tag_id")
    if isinstance(tag_id, bool) or not isinstance(tag_id, int):
        return jsonify({"error": "tag_id must be an integer"}), 400

    connection = get_db()
    try:
        game = connection.execute(
            "SELECT 1 FROM games WHERE game_id = ?", (game_id,)
        ).fetchone()
        if game is None:
            return jsonify({"error": "Game not found"}), 404
        
        tag = connection.execute(
            "SELECT 1 FROM tags WHERE tag_id = ?", (tag_id,)
        ).fetchone()
        if tag is None:
            return jsonify({"error": "Tag not found"}), 404
        
        try:
            connection.execute(
                "INSERT INTO game_tags (game_id, tag_id) VALUES (?, ?)",
                (game_id, tag_id),
            )
            connection.commit()
        except sqlite3.IntegrityError:
            return jsonify({"error": "tag is already attached to this game"}), 409
    finally:
        connection.close()

    return jsonify({"game_id": game_id, "tag_id": tag_id}), 201

# Delete game tag
@game_tags_bp.delete("/games/<int:game_id>/tags/<int:tag_id>")
def delete_game_tag(game_id, tag_id):
    connection = get_db()
    try:
        cursor=connection.execute(
            """
            DELETE FROM game_tags
            WHERE game_id = ? AND tag_id = ?
            """,
            (game_id, tag_id,),
        )
        connection.commit()

        row_count = cursor.rowcount
    finally:
        connection.close()

    if row_count == 0:
        return jsonify({"error": "Game tag not found"}), 404

    return jsonify({"message": "Game tag successfully deleted"})

# Search games by tag sorted by price
@game_tags_bp.get("/games/by-tag")
def search_by_tag():
    tag_name = request.args.get("tag","").strip()
    if not tag_name:
        return jsonify({"error": "tag query parameter is required"}), 400

    connection = get_db()
    try:
        games = connection.execute(
            """
            SELECT g.*
            FROM games g
            JOIN game_tags gt ON gt.game_id = g.game_id
            JOIN tags t ON t.tag_id = gt.tag_id
            WHERE t.name = ? COLLATE NOCASE
            ORDER BY g.price ASC, g.title ASC
            """,
            (tag_name,),
        ).fetchall()
    finally:
        connection.close()
   
    return jsonify([dict(game) for game in games])

# Search by publisher and tag
@game_tags_bp.get("/games/by-publisher-and-tag")
def search_by_publisher_and_tag():
    publisher = request.args.get("publisher", "").strip()
    tag_name = request.args.get("tag", "").strip()

    if not publisher or not tag_name:
        return jsonify({
            "error": "publisher and tag query parameters required"
        }), 400

    connection = get_db()
    try:
        games = connection.execute(
            """
            SELECT g.*
            FROM games g
            JOIN game_tags gt ON gt.game_id = g.game_id
            JOIN tags t ON t.tag_id = gt.tag_id
            WHERE g.publisher = ? COLLATE NOCASE AND t.name = ? COLLATE NOCASE
            ORDER BY g.title ASC
            """,
            (publisher, tag_name),
        ).fetchall()
    finally:
        connection.close()

    return jsonify([dict(game) for game in games])
    