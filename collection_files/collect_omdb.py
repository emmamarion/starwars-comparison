import requests
import sqlite3

import re


def get_api_key(filename="api_keys.txt"):
    """
    Returns the Api Key for the OMDB API.

    Args:
        filename (str, optinial): filename of textfile where api keys are stored

    Returns:
        api_key (str):
    """
    api_key = None
    try:
        with open(filename, "r") as f:
            text_file_contents = f.read().strip()
            api_key = re.search(r"omdb: (.*)", text_file_contents)
            if api_key:
                api_key = api_key.group(1)
                print("API KEY LOADED")
            else:
                print("WARNING: API key is not loaded.")

    except FileNotFoundError:
        print(f"ERROR: file: {filename} not found.")

    return api_key


def collect_omdb_data():
    pass


def insert_into_database(limit=25):
    pass


if __name__ == "__main__":
    API_KEY = get_api_key()
    print(API_KEY)
