import sqlite3

from flask import Blueprint, g, jsonify, request, session
from werkzeug.security import generate_password_hash

from gamevault.auth import (
    USER_COLUMNS, api_admin_required, api_user_access_required, log_in, public_user,
)
from gamevault.db import get_db

users_bp = Blueprint("users", __name__)

USER_FIELDS = ["username", "email"]


def validate_user_fields(data, fields):
    for field in fields:
        if not isinstance(data[field], str) or not data[field].strip():
            return f"{field} must be a non-empty string"

    if "email" in fields and "@" not in data["email"]:
        return "email must be a valid email address"

    return None


def validate_password(password):
    if not isinstance(password, str) or not password:
        return "password must not be empty"
    return None


def unique_field_error(error):
    for field in USER_FIELDS:
        if f"users.{field}" in str(error):
            return jsonify({"error": f"{field} is already taken"}), 409
    raise error


def find_user(connection, user_id):
    return public_user(connection.execute(
        f"SELECT {USER_COLUMNS} FROM users WHERE user_id = ?", (user_id,)
    ).fetchone())


@users_bp.post("/users")
def create_user():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be JSON"}), 400

    missing_fields = [field for field in USER_FIELDS + ["password"] if field not in data]
    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields,
        }), 400

    error = validate_user_fields(data, USER_FIELDS) or validate_password(data["password"])
    if error:
        return jsonify({"error": error}), 400

    connection = get_db()
    try:
        cursor = connection.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (data["username"].strip(), data["email"].strip(), generate_password_hash(data["password"])),
        )
        connection.commit()
        user = find_user(connection, cursor.lastrowid)
    except sqlite3.IntegrityError as e:
        return unique_field_error(e)
    finally:
        connection.close()

    if g.user is None:
        log_in(user["user_id"])

    return jsonify(user), 201


@users_bp.get("/users")
@api_admin_required
def list_users():
    connection = get_db()
    try:
        users = connection.execute(
            f"SELECT {USER_COLUMNS} FROM users ORDER BY user_id"
        ).fetchall()
    finally:
        connection.close()

    return jsonify([public_user(user) for user in users])


@users_bp.get("/users/<int:user_id>")
@api_user_access_required
def get_user(user_id):
    connection = get_db()
    try:
        user = find_user(connection, user_id)
    finally:
        connection.close()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user)


@users_bp.patch("/users/<int:user_id>")
@api_user_access_required
def update_user(user_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be JSON"}), 400

    fields = [field for field in USER_FIELDS if field in data]
    password = data.get("password") or None
    if not fields and password is None:
        return jsonify({
            "error": "Provide at least one field to update",
            "fields": USER_FIELDS + ["password"],
        }), 400

    error = validate_user_fields(data, fields)
    if not error and password is not None:
        error = validate_password(password)
    if error:
        return jsonify({"error": error}), 400

    assignments = [f"{field} = ?" for field in fields]
    values = [data[field].strip() for field in fields]
    if password is not None:
        assignments.append("password_hash = ?")
        values.append(generate_password_hash(password))

    connection = get_db()
    try:
        cursor = connection.execute(
            f"UPDATE users SET {', '.join(assignments)} WHERE user_id = ?",
            (*values, user_id),
        )
        connection.commit()
        user = find_user(connection, user_id)
    except sqlite3.IntegrityError as e:
        return unique_field_error(e)
    finally:
        connection.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user)


@users_bp.delete("/users/<int:user_id>")
@api_user_access_required
def delete_user(user_id):
    connection = get_db()
    try:
        user = find_user(connection, user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404
        if user["is_admin"]:
            return jsonify({"error": "Admin accounts can't be deleted"}), 403

        connection.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        connection.commit()
    finally:
        connection.close()

    if g.user["user_id"] == user_id:
        session.clear()

    return "", 204
