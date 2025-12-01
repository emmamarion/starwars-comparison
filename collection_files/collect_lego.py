import re


def get_api_key(filename="api_keys.txt"):
    api_key = None
    try:
        with open(filename, "r") as f:
            f.read()
            api_key = f.read().strip()
    except FileNotFoundError:
        print(f"ERROR: file: {filename} not found.")

    if api_key is None:
        print("WARNING: API key is not loaded.")

    return api_key
