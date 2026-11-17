DROP TABLE IF EXISTS game_tags;
DROP TABLE IF EXISTS library;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS games;

CREATE TABLE games (
    game_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    title        TEXT    NOT NULL,
    developer    TEXT    NOT NULL,
    publisher    TEXT    NOT NULL,
    release_date TEXT    NOT NULL,
    price        REAL    NOT NULL CHECK (price >= 0)
);

CREATE TABLE users (
    user_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    username   TEXT NOT NULL UNIQUE,
    email      TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tags (
    tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name   TEXT    NOT NULL UNIQUE COLLATE NOCASE
);

CREATE TABLE library (
    user_id    INTEGER NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
    game_id    INTEGER NOT NULL REFERENCES games (game_id) ON DELETE CASCADE,
    created_at TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, game_id)
);

CREATE TABLE game_tags (
    game_id INTEGER NOT NULL REFERENCES games (game_id) ON DELETE CASCADE,
    tag_id  INTEGER NOT NULL REFERENCES tags (tag_id)  ON DELETE CASCADE,
    PRIMARY KEY (game_id, tag_id)
);

CREATE INDEX idx_library_game    ON library (game_id);
CREATE INDEX idx_game_tags_tag   ON game_tags (tag_id);
CREATE INDEX idx_games_publisher ON games (publisher);
