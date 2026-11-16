import sqlite3
from pathlib import Path

import click

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
    finally:
        connection.close()
    click.echo(f"Initialized {DATABASE.name} with seed data")
