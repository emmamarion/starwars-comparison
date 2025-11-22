import requests
import sqlite3
import os

# NOTE:
# There are 82 people and 60 planets in swapi, which satisfies the
# "Access and store at least 100 rows in your database from each API/website" requirement

# People and planets each get their own seperate tables in the database, which satisfies the
# "For at least one API you must have two tables" requirement.

# The vehicle table contains a foriegn key from the planet table, which satisfies the
# "For at least one API you must have two tables that share an integer key" requirement.


# TODO: implement handling for "unknown" values
def get_data(type="vehicle", request_id=1):
    """
    creates an API request to the swapi and retreieves information for a SINGLE entry

    ARGUMENTS:
        type (string): specifies the type of request, either "starship" or "vehicle"
        request_id (int): the id of the vehicle
    RETURNS:
        data: json dictionary of requested data
    """

    # Set the base url for the request depending on the type argument
    base_url = (
        "https://swapi.info/api/starships/"
        if type.lower() == "starship"
        else "https://swapi.info/api/vehicles/"
    )

    # Convert the request id to a string to append to url
    vehicle_id_str = str(request_id)

    # Make the API request
    try:
        request_url = base_url + vehicle_id_str
        response = requests.get(request_url)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching API data: {e}")
        exit()


def update_vehicle_table(data, database_filename):
    """
    Adds vehicle data to the specified database in the "vehicles" table.

    ARGUMENTS:
        data (dict): json data for a vehicle
        database_filename (string): filename of the target database
    RETURNS:
        None
    """

    # Connect to SQLite database
    conn = sqlite3.connect(database_filename)
    cursor = conn.cursor()

    # Get and save vehicle information
    vehicle_name = data.get("name")
    vehicle_length = int(data.get("length"))
    vehicle_id = data.get("url", 0)[-2]

    cursor.execute(
        """INSERT INTO vehicles (id, name, vehicle_length) VALUES (?, ?, ?)""",
        (vehicle_id, vehicle_name, vehicle_length),
    )
    conn.commit()
    conn.close()


def update_planet_table(data, database_filename):
    # TODO: IMPLEMENT
    """
    Adds planet data to the specified database in the "planets" table.

    ARGUMENTS:
        data (dict): json data for a planet
        database_filename (string): filename of the target database
    RETURNS:
        None
    """
    # Connect to SQLite database
    conn = sqlite3.connect(database_filename)
    cursor = conn.cursor()

    planet_name = data.get("name")
    planet_population = data.get("population")
    planet_id = data.get("url", 0)[-2]
    planet_climate = data.get("climate")

    # Check if the row already exists
    cursor.execute("SELECT 1 FROM planets WHERE id = ?", (planet_id,))
    row_exists = cursor.fetchone()

    if row_exists:
        cursor.execute(
            """UPDATE planets SET name = ?, population = ? WHERE id = ?""",
            (planet_name, planet_population, planet_id),
        )
    else:
        cursor.execute(
            """INSERT INTO planets (id, name, population) VALUES (?, ?, ?)""",
            (planet_id, planet_name, planet_population),
        )
    conn.commit()
    conn.close()


# For debugging
def test():
    planet_data = get_data("planet", 3)
    update_planet_table(planet_data, "starwars.db")


if __name__ == "__main__":
    test()
