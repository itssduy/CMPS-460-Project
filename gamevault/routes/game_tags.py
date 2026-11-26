import sqlite3
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from flask import Blueprint, jsonify, request
from gamevault.auth import api_admin_required
from gamevault.db import get_db

game_tags_bp = Blueprint("game_tags", __name__)

# Attatch a tag to a game
@game_tags_bp.post("/games/<int:game_id>/tags")
@api_admin_required
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
@api_admin_required
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

 # Put a game on sale with a percentage discount and discount tag
@game_tags_bp.post("/games/<int:game_id>/sale")
@api_admin_required
def put_game_on_sale(game_id):
    raw_discount = request.args.get("discount_percent")
    if raw_discount is None:
        return jsonify({"error": "discount_percent query parameter is required"}), 400

    try:
        discount_percent = Decimal(raw_discount)
    except InvalidOperation:
        return jsonify({"error": "discount_percent must be a number from 0 to 100"}), 400

    if not discount_percent.is_finite() or not Decimal("0") < discount_percent <= Decimal("100"):
        return jsonify({"error": "discount_percent must be greater than 0 and at most 100"}), 400

    connection = get_db()
    try:
        game = connection.execute(
            "SELECT price FROM games WHERE game_id = ?", (game_id,)
        ).fetchone()
        if game is None:
            return jsonify({"error": "Game not found"}), 404

        discount_tag = connection.execute(
            "SELECT tag_id FROM tags WHERE name = ? COLLATE NOCASE",
            ("Discount",),
        ).fetchone()
        if discount_tag is None:
            return jsonify({"error": "Discount tag not found"}), 404

        already_on_sale = connection.execute(
            "SELECT 1 FROM game_tags WHERE game_id = ? AND tag_id = ?",
            (game_id, discount_tag["tag_id"]),
        ).fetchone()
        if already_on_sale:
            return jsonify({"error": "Game is already on sale"}), 409

        original_price = Decimal(str(game["price"]))
        sale_price = (original_price * (Decimal("100") - discount_percent) / Decimal("100"))
        sale_price = sale_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        try:
            connection.execute(
                "INSERT INTO game_tags (game_id, tag_id) VALUES (?, ?)",
                (game_id, discount_tag["tag_id"]),
            )
            connection.execute(
                "UPDATE games SET price = ? WHERE game_id = ?",
                (float(sale_price), game_id),
            )
            connection.commit()
        except sqlite3.IntegrityError:
            return jsonify({"error": "Game is already on sale"}), 409
    finally:
        connection.close()

    return jsonify({
        "game_id": game_id,
        "tag_id": discount_tag["tag_id"],
        "sale": True,
        "discount_percent": float(discount_percent),
        "price": float(sale_price),
    }), 201
