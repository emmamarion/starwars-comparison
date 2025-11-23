import os
import json


def load_cache(filename):
    """
    Load a JSON cache file if it exists

    ARGUMENTS:
        filename (str): name of the file to be loaded.

    RETURNS:
        loaded data.
    """
    if os.path.exists(filename):
        print(f"Loading data from cache: {filename}")
        try:
            with open(filename, "r") as f:
                loaded_json = json.load(f)
            return loaded_json
        except IOError as e:
            print(f"WARNING Could not load cache file: {e}")
    else:
        print(f"No file with {filename} exists at that path")
        return None


def save_cache(data, filename):
    """
    Encodes dictonary into JSON format and writes
    the JSON to filename to save the search results

    ARGUMENTS:
        data (list or dict): data to be written to a JSON file
        filename (str): the name of the file to write a cache to

    RETURNS:
        None
    """

    root, extension = os.path.splitext(filename)
    if extension == ".json":
        try:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
                print(f"Saved data to cache: {filename}")
        except IOError as e:
            print(f"WARNING Could not save cache file: {e}")
    else:
        print(f"ERROR - The file provided: {filename} is not a json filetype")
