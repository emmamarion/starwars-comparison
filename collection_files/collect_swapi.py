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
    RETURNS:
        data: json dictionary of requested data
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
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching API data: {e}")
        exit()


def update_character_table(data, database_filename):
    # TODO: create docstring for function

    # Connect to SQLite database
    conn = sqlite3.connect(database_filename)
    cursor = conn.cursor()

    # Get and save character information
    character_name = data.get("name", 0)
    character_height = int(data.get("height", 0))
    character_id = data.get("url", 0)[-2]
    character_homeworld_id = (data.get("homeworld", 0))[-2]

    cursor.execute(
        """INSERT INTO characters (id, name, height, homeworld_id) VALUES (?, ?, ?, ?)""",
        (character_id, character_name, character_height, character_homeworld_id),
    )
    conn.commit()
    conn.close()


# For debugging
def test():
    char_data = get_data("character", 1)
    update_character_table(char_data, "starwars.db")


if __name__ == "__main__":
    test()
