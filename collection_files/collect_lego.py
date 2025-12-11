import re


def get_api_key(filename="api_keys.txt"):
    """
    Returns the Api Key for the Rebrickable API.

    Args:
        filename (str, optinial): filename of textfile where api keys are stored

    Returns:
        api_key (str):
    """
    api_key = None
    try:
        with open(filename, "r") as f:
            text_file_contents = f.read().strip()
            api_key = re.search(r"rebrickable: (.*)", text_file_contents)
            if api_key:
                api_key = api_key.group(1)
                print("API KEY LOADED")
            else:
                print("WARNING: API key is not loaded.")

    except FileNotFoundError:
        print(f"ERROR: file: {filename} not found.")

    return api_key


if __name__ == "__main__":
    API_KEY = get_api_key()
    print(API_KEY)


DB_NAME = "starwars.db"
BASE_URL = "https://rebrickable.com/api/v3/lego/sets/"
LIMIT_PER_RUN = 25   # rubric: max 25 rows per run
TARGET_TOTAL = 100   # rubric: at least 100 rows total


def create_lego_table(db_filename=DB_FILENAME):
    """
    Creates the lego_sets table if it doesn't already exist.

    We do this here (like MovieMetrics in collect_omdb.py) so we don't have
    to modify database_setup.py.
    """
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS lego_sets (
            set_num TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            year INTEGER,
            num_parts INTEGER
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
        # you could optionally filter by theme, e.g. search="Star Wars"
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.RequestException as e:
        print(f"Error fetching Lego sets: {e}")
        return []


def insert_lego_sets(limit=25, db_filename=DB_FILENAME):
    """
    Inserts Lego set data into the database, limiting to `limit`
    NEW entries per run.

    - Creates lego_sets table if it does not exist
    - Does NOT insert duplicate set_num values
    - You can run this multiple times until 100+ rows exist

    Args:
        limit (int): maximum number of *new* rows to insert this run

    Returns:
        int: number of Lego sets added this run
    """
    api_key = get_api_key()
    if not api_key:
        print("No Rebrickable API key found; aborting Lego collection.")
        return 0

    # Ensure table exists
    create_lego_table(db_filename)

    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # How many Lego sets already in DB?
    cursor.execute("SELECT COUNT(*) FROM lego_sets")
    current_count = cursor.fetchone()[0]
    print(f"Current Lego rows in DB: {current_count}")

    if current_count >= 100:
        print("✅ Already have 100+ Lego sets. No additional data needed.")
        conn.close()
        return 0

    # Fetch a big page of sets; we will still only insert up to `limit`
    lego_sets = fetch_lego_sets(api_key, page_size=100, page=1)
    if not lego_sets:
        print("No Lego data fetched from API.")
        conn.close()
        return 0

    rows_added = 0
    print(f"Fetched {len(lego_sets)} Lego sets from API. Processing with limit {limit}...")

    for lego_set in lego_sets:
        if rows_added >= limit:
            print(f"Reached limit of {limit} new Lego rows this run.")
            break

        set_num = lego_set.get("set_num")
        name = lego_set.get("name")
        year = lego_set.get("year")
        num_parts = lego_set.get("num_parts")

        if not set_num:
            continue  # skip weird / incomplete rows

        # Skip if already in DB (prevents duplicates)
        cursor.execute("SELECT 1 FROM lego_sets WHERE set_num = ?", (set_num,))
        if cursor.fetchone():
            continue

        cursor.execute(
            """
            INSERT INTO lego_sets (set_num, name, year, num_parts)
            VALUES (?, ?, ?, ?)
            """,
            (set_num, name, year, num_parts),
        )
        rows_added += 1
        print(f"Added Lego set: {set_num} - {name} ({num_parts} parts)")

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
