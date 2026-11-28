from flask import Blueprint, abort, current_app, g, jsonify, redirect, request, url_for
from gamevault.auth import api_user_access_required, page_user_access_required
from gamevault.db import get_db
from gamevault.steam import SteamError, import_library, login_url, verify_login

steam_bp = Blueprint("steam", __name__)


def callback_url(user_id):
    return url_for("steam.steam_callback", user_id=user_id, _external=True)


def find_user(connection, user_id):
    return connection.execute(
        "SELECT user_id, steam_id FROM users WHERE user_id = ?", (user_id,)
    ).fetchone()


@steam_bp.get("/users/<int:user_id>/steam/login")
@page_user_access_required
def steam_login(user_id):
    if g.user["user_id"] != user_id:
        abort(403)

    connection = get_db()
    try:
        user = find_user(connection, user_id)
    finally:
        connection.close()

    if user is None:
        return redirect(url_for("pages.users"))

    return redirect(login_url(callback_url(user_id), request.host_url))


@steam_bp.get("/users/<int:user_id>/steam/callback")
@page_user_access_required
def steam_callback(user_id):
    if g.user["user_id"] != user_id:
        abort(403)

    def back_to_profile(message):
        return redirect(url_for("pages.user_profile", user_id=user_id, steam_error=message))

    try:
        steam_id = verify_login(request.args.to_dict(), callback_url(user_id))
    except SteamError as error:
        return back_to_profile(str(error))

    connection = get_db()
    try:
        if find_user(connection, user_id) is None:
            return redirect(url_for("pages.users"))

        owner = connection.execute(
            "SELECT user_id FROM users WHERE steam_id = ?", (steam_id,)
        ).fetchone()
        if owner and owner["user_id"] != user_id:
            return back_to_profile("That Steam account is already linked to another user.")

        connection.execute(
            "UPDATE users SET steam_id = ? WHERE user_id = ?", (steam_id, user_id)
        )
        connection.commit()

        try:
            summary = import_library(
                connection, user_id, steam_id, current_app.config.get("STEAM_API_KEY")
            )
        except SteamError as error:
            return back_to_profile(f"Steam account linked, but the import failed: {error}")
    finally:
        connection.close()

    return redirect(url_for("pages.user_library", user_id=user_id, **{
        f"steam_{key}": value for key, value in summary.items()
    }))


@steam_bp.post("/api/users/<int:user_id>/steam/import")
@api_user_access_required
def steam_import(user_id):
    connection = get_db()
    try:
        user = find_user(connection, user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404
        if not user["steam_id"]:
            return jsonify({"error": "This user hasn't linked a Steam account"}), 400

        try:
            summary = import_library(
                connection, user_id, user["steam_id"], current_app.config.get("STEAM_API_KEY")
            )
        except SteamError as error:
            return jsonify({"error": str(error)}), 502
    finally:
        connection.close()

    return jsonify(summary)


@steam_bp.delete("/api/users/<int:user_id>/steam")
@api_user_access_required
def steam_unlink(user_id):
    connection = get_db()
    try:
        cursor = connection.execute(
            "UPDATE users SET steam_id = NULL WHERE user_id = ?", (user_id,)
        )
        connection.commit()
    finally:
        connection.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "User not found"}), 404

    return "", 204
