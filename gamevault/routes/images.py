import uuid
from pathlib import Path

from flask import Blueprint, current_app, jsonify, request
from gamevault.db import get_db

images_bp = Blueprint("images", __name__)

UPLOAD_PREFIX = "/static/uploads/"


def detect_image_type(header):
    if header.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if header[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    if header[:4] == b"RIFF" and header[8:12] == b"WEBP":
        return "webp"
    return None


def upload_dir():
    path = Path(current_app.static_folder) / "uploads"
    path.mkdir(exist_ok=True)
    return path


@images_bp.post("/games/<int:game_id>/image")
def upload_game_image(game_id):
    file = request.files.get("image")
    if file is None or not file.filename:
        return jsonify({"error": "Choose an image to upload"}), 400

    extension = detect_image_type(file.stream.read(12))
    file.stream.seek(0)
    if extension is None:
        return jsonify({"error": "Image must be a JPG, PNG, WebP, or GIF"}), 400

    connection = get_db()
    try:
        game = connection.execute(
            "SELECT image_url FROM games WHERE game_id = ?", (game_id,)
        ).fetchone()
        if game is None:
            return jsonify({"error": "Game not found"}), 404

        filename = f"{uuid.uuid4().hex}.{extension}"
        file.save(upload_dir() / filename)
        image_url = UPLOAD_PREFIX + filename

        connection.execute(
            "UPDATE games SET image_url = ? WHERE game_id = ?", (image_url, game_id)
        )
        connection.commit()
    finally:
        connection.close()

    old_url = game["image_url"] or ""
    if old_url.startswith(UPLOAD_PREFIX):
        (upload_dir() / old_url.removeprefix(UPLOAD_PREFIX)).unlink(missing_ok=True)

    return jsonify({"game_id": game_id, "image_url": image_url}), 201
