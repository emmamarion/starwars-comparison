# collect_lego.py
# Author: Ava
# Purpose: Collect Lego sets from the Rebrickable API and store them in starwars.db


import re
import requests
import sqlite3

DB_NAME = "starwars.db"
BASE_URL = "https://rebrickable.com/api/v3/lego/sets/"
LIMIT_PER_RUN = 25  # rubric: max 25 rows per run
TARGET_TOTAL = 100  # rubric: at least 100 rows total


def get_api_key(filename="api_keys.txt"):
    """
    Returns the Api Key for the Rebrickable API.

    Args:
        filename (str, optional): filename of textfile where api keys are stored

    Returns:
        api_key (str) or None
    """
    api_key = None
    try:
        with open(filename, "r") as f:
            text_file_contents = f.read().strip()
            api_key = re.search(r"rebrickable: (.*)", text_file_contents)
            if api_key:
                api_key = api_key.group(1)
                print("Rebrickable API KEY LOADED")
            else:
                print("WARNING: Rebrickable API key is not loaded.")

    except FileNotFoundError:
        print(f"ERROR: file: {filename} not found.")

    return api_key

def create_lego_tables(db_filename=DB_NAME):
    """
    Creates the lego_sets and lego_themes tables if they don't already exist.

    lego_themes:
        id  INTEGER PRIMARY KEY      (matches Rebrickable theme_id)
        name TEXT UNIQUE NULL        (optional – we can add later)

    lego_sets:
        set_num  TEXT PRIMARY KEY
        name     TEXT NOT NULL
        year     INTEGER
        num_parts INTEGER
        theme_id INTEGER REFERENCES lego_themes(id)
    """
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Theme table (one row per theme_id)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS lego_themes (
            id   INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
        """
    )

    # Lego sets table, now with theme_id as integer
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS lego_sets (
            set_num   TEXT PRIMARY KEY,
            name      TEXT NOT NULL,
            year      INTEGER,
            num_parts INTEGER,
            theme_id  INTEGER,
            FOREIGN KEY(theme_id) REFERENCES lego_themes(id)
        )
        """
    )

    conn.commit()
    conn.close()

def fetch_lego_sets(api_key, page_size=100, page=1):
    """
    Fetches Lego sets from the Rebrickable API.

    Args:
        api_key (str): Rebrickable API key
        page_size (int): number of results per page (request side)
        page (int): which page to request

    Returns:
        list[dict]: list of Lego set dictionaries
    """
    headers = {"Authorization": f"key {api_key}"}
    params = {
        "page_size": page_size,
        "page": page,
        #could optionally filter by theme, e.x search = "Star Wars"
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.RequestException as e:
        print(f"Error fetching Lego sets: {e}")
        return []


def insert_lego_sets(limit=25, db_filename=DB_NAME):
    """
    Inserts Lego set data into the database, limiting to `limit`
    NEW entries per run.

    Now also populates lego_themes so that lego_sets.theme_id
    links to lego_themes.id (shared integer key).
    """
    api_key = get_api_key()
    if not api_key:
        print("No Rebrickable API key found; aborting Lego collection.")
        return 0

    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # How many Lego sets already in DB?
    cursor.execute("SELECT COUNT(*) FROM lego_sets")
    current_count = cursor.fetchone()[0]
    print(f"Current Lego rows in DB: {current_count}")

    if current_count >= 100:
        print("Already have 100+ Lego sets. No additional data needed.")
        conn.close()
        return 0

    # Fetch a big page of sets, we will still only insert up to `limit`
    lego_sets = fetch_lego_sets(api_key, page_size=100, page=1)
    if not lego_sets:
        print("No Lego data fetched from API.")
        conn.close()
        return 0

    rows_added = 0
    print(
        f"Fetched {len(lego_sets)} Lego sets from API. Processing with limit {limit}..."
    )

    for lego_set in lego_sets:
        if rows_added >= limit:
            print(f"Reached limit of {limit} new Lego rows this run.")
            break

        set_num = lego_set.get("set_num")
        name = lego_set.get("name")
        year = lego_set.get("year")
        num_parts = lego_set.get("num_parts")
        theme_id = lego_set.get("theme_id")  # from API

        if not set_num:
            continue  # skip weird or incomplete rows

        # Ensure the theme exists in lego_themes (integer key)
        if theme_id is not None:
            cursor.execute(
                "INSERT OR IGNORE INTO lego_themes (id) VALUES (?)",
                (theme_id,theme_name),
            )

        # Skip if set already exists in lego_sets
        cursor.execute("SELECT 1 FROM lego_sets WHERE set_num = ?", (set_num,))
        if cursor.fetchone():
            continue

        # Insert set, storing theme_id as integer FK
        cursor.execute(
            """
            INSERT INTO lego_sets (set_num, name, year, num_parts, theme_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (set_num, name, year, num_parts, theme_id),
        )
        rows_added += 1
        print(
            f"Added Lego set: {set_num} - {name} ({num_parts} parts, theme_id={theme_id})"
        )

    conn.commit()
    conn.close()

    # Show total after insert
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM lego_sets")
    new_total = cursor.fetchone()[0]
    conn.close()

    print(f"\n{'=' * 60}")
    print(f"Lego sets added this run: {rows_added}")
    print(f"Total Lego sets in database now: {new_total}")
    print(f"{'=' * 60}\n")

    return rows_added


if __name__ == "__main__":
    # For testing this file directly:
    added = insert_lego_sets(limit=25)
    print(f"Job complete. Total new Lego sets added: {added}")

    #pushing for emma
