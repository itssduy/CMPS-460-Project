import sqlite3
from flask import Blueprint, jsonify, request
from gamevault.db import get_db

tags_bp = Blueprint("tags", __name__)

# Create a tag
@tags_bp.post("/tags")
def create_tag():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be JSON"}), 400

    if "name" not in data:
            return jsonify ({
                "error": "Missing required fields",
                "field": "name",
            }), 400

    name = data["name"]
    if not isinstance(name, str) or not name.strip():
         return jsonify ({
             "error": "name must not be an empty string",
         }), 400

    name = name.strip()
    connection = get_db()
    try:
        cursor = connection.execute(
            """
            INSERT INTO tags (name)
            VALUES (?)
            """,
            (
               name,
            ),
        )
        connection.commit()
        tag_id = cursor.lastrowid
    except sqlite3.IntegrityError:
         return jsonify({"error": "Tag already exists"}), 409
    finally:
        connection.close()
    
    return jsonify({
        "tag_id": tag_id,
        "name": name,
    }), 201

# List all tags
@tags_bp.get("/tags")
def list_tags():
    connection = get_db()

    try:
        data = connection.execute(
            """
            SELECT *
            FROM tags
            """    
        ).fetchall()
        connection.commit()
    finally:
        connection.close()

    return jsonify([dict(row) for row in data])

# Get specific tag
@tags_bp.get("/tags/<int:tag_id>")
def get_tag(tag_id):
    connection=get_db()

    try:
        data = connection.execute(
            """
            SELECT *
            FROM tags
            WHERE tag_id = ?
            """,
            (tag_id,),
        ).fetchone()
        connection.commit()
    finally:
        connection.close()

    if data is None:
        return jsonify({"error": "Tag not found"}), 404

    return jsonify(dict(data))

# Update Tags
@tags_bp.patch("/tags/<int:tag_id>")
def update_tag(tag_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be in JSON"}), 400

    if "name" not in data:
        return jsonify({
            "error": "Missing required field",
            "field": "name",
        }), 400

    name = data["name"]
    if not isinstance(name, str) or not name.strip():
        return jsonify ({
             "error": "name must not be an empty string",
        }), 400

    name = name.strip()
    connection = get_db()
    try:
        cursor = connection.execute(
            """
            UPDATE tags
            SET name = ?
            WHERE tag_id = ?
            """,
            (
                name,
                tag_id,
            ),
        )
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Tag not found"}), 404

        updated_tag = connection.execute(
            "SELECT * FROM tags WHERE tag_id = ?",
            (tag_id,),
        ).fetchone()
    except sqlite3.IntegrityError:
         return jsonify({"error": "Tag already exists"}), 409
    finally:
        connection.close()

    return jsonify(dict(updated_tag))

# Delete tag
@tags_bp.delete("/tags/<int:tag_id>")
def delete_tag(tag_id):
    connection = get_db()

    try:
        cursor=connection.execute(
            """
            DELETE FROM tags
            WHERE tag_id = ?
            """,
            (tag_id,),
        )
        connection.commit()

        row_count = cursor.rowcount
    finally:
        connection.close()

    if row_count == 0:
        return jsonify({"error": "Tag not found"}), 404

    return jsonify({"message": "Tag successfully deleted"})
