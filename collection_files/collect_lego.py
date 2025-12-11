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

