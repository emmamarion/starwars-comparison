import requests
import sqlite3
import os

# NOTE:
# There are 82 people and 60 planets in swapi, which satisfies the
# "Access and store at least 100 rows in your database from each API/website" requirement

# People and planets each get their own seperate tables in the database
# The character table contains a foriegn key from the planet table


def get_data(type="character", request_id=1):
    """
    creates an API request to the swapi and retreieves information for a SINGLE entry
    ARGUMENTS:
        type (string): specifies the type of request, either "character" or "planet"
        request_id (int): the id of the character
    """

    # Set the base url for the request depending on the type argument
    base_url = (
        "http://swapi.dev/api/people/"
        if type.lower() == "character"
        else "http://swapi.dev/api/planet/"
    )

    # Convert the request id to a string to append to url
    character_id_str = str(request_id)

    # Make the API request
    try:
        request_url = base_url + character_id_str
        response = requests.get(request_url)
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching API data: {e}")
        exit()

    # TODO Connect to SQLite database
    pass


# For debugging
def test():
    get_data()


test()
