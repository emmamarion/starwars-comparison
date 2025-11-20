import requests
import sqlite3
import os


def get_character(character_id=1):
    """
    creates an API request to the swapi
    ARGUMENTS:
        character_id: the id of the character
    """

    base_url = "http://swapi.dev/api/people/"

    # convert the character id to a string to append to url
    character_id_str = str(character_id)

    # Make the API request
    try:
        request_url = base_url + character_id_str
        response = requests.get(request_url)
        character_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching API data: {e}")
        exit()

    # Connect to SQLite database
    pass


# For debugging
def test():
    get_character()


test()
