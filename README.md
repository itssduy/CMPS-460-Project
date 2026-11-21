# GameVault

A video game storefront database for CMPS 460.

## Setup

```
uv sync
uv run flask --app gamevault init-db
uv run flask --app gamevault run
```

`init-db` creates `games.db` from `sql/schema.sql` and `sql/seed.sql`. Run it again any time to reset the data.

## Layout

```
gamevault/
  __init__.py   app setup
  db.py         database connection and init-db command
  routes/       API endpoints under /api, plus pages.py for the site pages
  templates/    Jinja templates (base.html is the shared layout)
  static/       CSS
sql/
  schema.sql
  seed.sql
```
