# GameVault

A video game storefront database for CMPS 460.

## Setup

```
uv sync
uv run flask --app gamevault init-db
uv run flask --app gamevault run
```

`init-db` creates `games.db` from `sql/schema.sql` and `sql/seed.sql` and an `admin` account. Run it again any time to reset the data.

## Settings

Put these in a `.env` file in the project root (git ignores it):

```
SECRET_KEY=any_long_random_string
ADMIN_PASSWORD=password_for_the_admin_account
STEAM_API_KEY=your_steam_web_api_key
```

`SECRET_KEY` keeps people logged in across server restarts. If `ADMIN_PASSWORD` is missing, `init-db` makes a random one and prints it.

## Steam import

Users can sign in through Steam on their profile page to import the games they own.
This needs a Steam Web API key (free at https://steamcommunity.com/dev/apikey).
Put it in a `.env` file in the project root, which git ignores:

```
STEAM_API_KEY=your_key_here
```

Restart the server after adding it. The player's Steam profile must have game details set to public.

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
