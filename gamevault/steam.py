import json
import re
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

OPENID_URL = "https://steamcommunity.com/openid/login"
OPENID_NS = "http://specs.openid.net/auth/2.0"
IDENTIFIER_SELECT = "http://specs.openid.net/auth/2.0/identifier_select"
CLAIMED_ID = re.compile(r"^https://steamcommunity\.com/openid/id/(\d{17})$")

OWNED_GAMES_URL = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
APP_DETAILS_URL = "https://store.steampowered.com/api/appdetails"

MAX_NEW_GAMES = 100

CATEGORY_TAGS = {
    "Single-player": "Singleplayer",
    "Multi-player": "Multiplayer",
    "Online PvP": "Multiplayer",
    "Co-op": "Co-op",
    "Online Co-op": "Co-op",
    "Shared/Split Screen Co-op": "Co-op",
}

DATE_FORMATS = ["%b %d, %Y", "%d %b, %Y", "%B %d, %Y", "%d %B, %Y", "%b %Y", "%B %Y", "%Y"]


class SteamError(Exception):
    pass


def _request(url, params=None, data=None):
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, data=data, headers={"User-Agent": "GameVault"})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.read().decode()
    except urllib.error.HTTPError as error:
        if error.code == 403:
            raise SteamError("Steam rejected the API key. Check STEAM_API_KEY.") from error
        raise SteamError(f"Steam returned an error ({error.code}). Try again later.") from error
    except urllib.error.URLError as error:
        raise SteamError("Couldn't reach Steam. Try again later.") from error


def login_url(return_to, realm):
    params = {
        "openid.ns": OPENID_NS,
        "openid.mode": "checkid_setup",
        "openid.return_to": return_to,
        "openid.realm": realm,
        "openid.identity": IDENTIFIER_SELECT,
        "openid.claimed_id": IDENTIFIER_SELECT,
    }
    return f"{OPENID_URL}?{urllib.parse.urlencode(params)}"


def verify_login(params, expected_return_to):
    if params.get("openid.mode") != "id_res":
        raise SteamError("Steam sign-in was cancelled.")

    if params.get("openid.return_to", "").split("?")[0] != expected_return_to:
        raise SteamError("Steam sign-in didn't match this page. Try again.")

    match = CLAIMED_ID.match(params.get("openid.claimed_id", ""))
    if not match:
        raise SteamError("Steam didn't return a valid account.")

    check = {key: value for key, value in params.items() if key.startswith("openid.")}
    check["openid.mode"] = "check_authentication"
    body = _request(OPENID_URL, data=urllib.parse.urlencode(check).encode())
    if "is_valid:true" not in body.splitlines():
        raise SteamError("Steam couldn't verify the sign-in. Try again.")

    return match.group(1)


def owned_games(api_key, steam_id):
    data = json.loads(_request(OWNED_GAMES_URL, {
        "key": api_key,
        "steamid": steam_id,
        "include_appinfo": 1,
        "include_played_free_games": 1,
    }))
    response = data.get("response", {})

    if "games" in response:
        return response["games"]
    if response.get("game_count") == 0:
        return []
    raise SteamError(
        "Couldn't read this Steam library. Set the Steam profile's game details to public and try again."
    )


def app_details(app_id):
    try:
        data = json.loads(_request(APP_DETAILS_URL, {"appids": app_id, "cc": "us", "l": "english"}))
    except (SteamError, ValueError):
        return None
    entry = (data or {}).get(str(app_id)) or {}
    return entry.get("data") if entry.get("success") else None


def parse_release_date(text):
    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(text.strip(), date_format).date().isoformat()
        except ValueError:
            continue
    return None


def first_name(names):
    return next((name.strip() for name in names or [] if name and name.strip()), None)


def game_from_details(details):
    if not details or details.get("type") != "game" or not details.get("name"):
        return None

    release_date = parse_release_date(details.get("release_date", {}).get("date", ""))
    if release_date is None:
        return None

    developer = first_name(details.get("developers")) or "Unknown"
    publisher = first_name(details.get("publishers")) or developer

    if details.get("is_free"):
        price = 0.0
    else:
        price = details.get("price_overview", {}).get("initial", 0) / 100

    tag_names = {genre["description"] for genre in details.get("genres", [])}
    for category in details.get("categories", []):
        if category["description"] in CATEGORY_TAGS:
            tag_names.add(CATEGORY_TAGS[category["description"]])

    return {
        "title": details["name"],
        "developer": developer,
        "publisher": publisher,
        "release_date": release_date,
        "price": price,
        "image_url": details.get("header_image"),
        "tags": tag_names,
    }


def find_games_by_app_id(connection, app_ids):
    found = {}
    for start in range(0, len(app_ids), 500):
        chunk = app_ids[start:start + 500]
        placeholders = ", ".join("?" for _ in chunk)
        rows = connection.execute(
            f"SELECT game_id, steam_app_id FROM games WHERE steam_app_id IN ({placeholders})",
            chunk,
        ).fetchall()
        found.update({row["steam_app_id"]: row["game_id"] for row in rows})
    return found


def import_library(connection, user_id, steam_id, api_key):
    if not api_key:
        raise SteamError("Steam import isn't set up yet. Add STEAM_API_KEY to the server's .env file.")

    owned = sorted(owned_games(api_key, steam_id), key=lambda game: game.get("playtime_forever", 0), reverse=True)
    app_ids = [game["appid"] for game in owned]
    catalog = find_games_by_app_id(connection, app_ids)

    missing = [app_id for app_id in app_ids if app_id not in catalog]
    to_create = missing[:MAX_NEW_GAMES]
    with ThreadPoolExecutor(max_workers=8) as pool:
        details = list(pool.map(app_details, to_create))

    tag_ids = {row["name"].lower(): row["tag_id"] for row in connection.execute("SELECT tag_id, name FROM tags")}
    steam_platform = connection.execute(
        "SELECT platform_id FROM platforms WHERE name = 'Steam'"
    ).fetchone()

    created = 0
    skipped = 0
    for app_id, info in zip(to_create, details):
        game = game_from_details(info)
        if game is None:
            skipped += 1
            continue

        cursor = connection.execute(
            """
            INSERT INTO games (title, developer, publisher, release_date, price, image_url, steam_app_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (game["title"], game["developer"], game["publisher"], game["release_date"],
             game["price"], game["image_url"], app_id),
        )
        game_id = cursor.lastrowid
        catalog[app_id] = game_id
        created += 1

        if steam_platform:
            connection.execute(
                "INSERT OR IGNORE INTO game_platforms (game_id, platform_id) VALUES (?, ?)",
                (game_id, steam_platform["platform_id"]),
            )
        for name in game["tags"]:
            if name.lower() in tag_ids:
                connection.execute(
                    "INSERT OR IGNORE INTO game_tags (game_id, tag_id) VALUES (?, ?)",
                    (game_id, tag_ids[name.lower()]),
                )

    added = 0
    for app_id in app_ids:
        if app_id in catalog:
            cursor = connection.execute(
                "INSERT OR IGNORE INTO library (user_id, game_id) VALUES (?, ?)",
                (user_id, catalog[app_id]),
            )
            added += cursor.rowcount

    connection.commit()

    return {
        "owned_on_steam": len(app_ids),
        "added_to_library": added,
        "new_catalog_games": created,
        "skipped": skipped,
        "not_imported_yet": len(missing) - len(to_create),
    }
