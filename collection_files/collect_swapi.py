import requests
import sqlite3
import os

# NOTE:
# There are 39 vehicles and 75 starships in swapi. We're treating them both as "vehicles"
# and storing them in one table with over over 100 rows, which satisfies the
# "Access and store at least 100 rows in your database from each API/website" requirement

# Vehicles and manufacturers each get their own seperate tables in the database, which satisfies the
# "For at least one API you must have two tables" requirement.

# The vehicle table contains a foriegn key from the manufacturer table, which satisfies the
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


def update_manufacturer_table(data, database_filename):
    # TODO: IMPLEMENT
    """
    Adds manufacturer data to the specified database in the "manufacturers" table.

    ARGUMENTS:
        data (dict): json data for a vehicle
        database_filename (string): filename of the target database
    RETURNS:
        None
    """
    # Connect to SQLite database
    conn = sqlite3.connect(database_filename)
    cursor = conn.cursor()

    manufacturer_name = data.get("name")
    manufacturer_population = data.get("population")
    manufacturer_id = data.get("url", 0)[-2]
    manufacturer_climate = data.get("climate")

    # Check if the row already exists
    cursor.execute("SELECT 1 FROM manufacturers WHERE id = ?", (manufacturer_id,))
    row_exists = cursor.fetchone()

    if row_exists:
        cursor.execute(
            """UPDATE manufacturers SET name = ?, population = ? WHERE id = ?""",
            (manufacturer_name, manufacturer_population, manufacturer_id),
        )
    else:
        cursor.execute(
            """INSERT INTO manufacturers (id, name, population) VALUES (?, ?, ?)""",
            (manufacturer_id, manufacturer_name, manufacturer_population),
        )
    conn.commit()
    conn.close()


# For debugging
def test():
    manufacturer_data = get_data("manufacturer", 3)
    update_manufacturer_table(manufacturer_data, "starwars.db")


if __name__ == "__main__":
    test()
