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


def collect_lego_sets(db_name=DB_NAME):
    """
    Fetch Lego sets from the Rebrickable API and insert up to 25 NEW rows
    into the lego_sets table in the SQLite database.

    - Does NOT insert duplicates (based on set_num)
    - Stops once 100 or more rows exist in the table
    """
    api_key = get_api_key()
    if not api_key:
        print("ERROR: Missing Rebrickable API key.")
        return