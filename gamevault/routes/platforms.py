from flask import Blueprint, jsonify
from gamevault.db import get_db

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
