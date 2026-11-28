import sqlite3
from pathlib import Path

import click
from werkzeug.security import generate_password_hash

ROOT = Path(__file__).resolve().parent.parent
DATABASE = ROOT / "games.db"
SQL_DIR = ROOT / "sql"


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


@click.command("init-db")
def init_db():
    connection = get_db()
    try:
        connection.executescript((SQL_DIR / "schema.sql").read_text())
        connection.executescript((SQL_DIR / "seed.sql").read_text())

        password = "password"
        connection.execute(
            """
            INSERT INTO users (username, password_hash, is_admin)
            VALUES ('admin', ?, 1)
            """,
            (generate_password_hash(password),),
        )
        connection.commit()
    finally:
        connection.close()

    click.echo(f"Initialized {DATABASE.name} with seed data")


def attach_platforms(connection, games):
    games = [dict(game) for game in games]
    if not games:
        return games

    ids = [game["game_id"] for game in games]
    placeholders = ", ".join("?" for _ in ids)
    rows = connection.execute(
        f"""
        SELECT gp.game_id, p.name
        FROM game_platforms gp
        JOIN platforms p ON p.platform_id = gp.platform_id
        WHERE gp.game_id IN ({placeholders})
        ORDER BY p.platform_id
        """,
        ids,
    ).fetchall()

    platforms = {}
    for row in rows:
        platforms.setdefault(row["game_id"], []).append(row["name"])

    for game in games:
        game["platforms"] = platforms.get(game["game_id"], [])
    return games


def attach_tags(connection, games):
    games = [dict(game) for game in games]
    if not games:
        return games

    ids = [game["game_id"] for game in games]
    placeholders = ", ".join("?" for _ in ids)
    rows = connection.execute(
        f"""
        SELECT gt.game_id, t.tag_id, t.name
        FROM game_tags gt
        JOIN tags t ON t.tag_id = gt.tag_id
        WHERE gt.game_id IN ({placeholders})
        ORDER BY t.name
        """,
        ids,
    ).fetchall()

    tags = {}
    for row in rows:
        tags.setdefault(row["game_id"], []).append(
            {"tag_id": row["tag_id"], "name": row["name"]}
        )

    for game in games:
        game["tags"] = tags.get(game["game_id"], [])
    return games
