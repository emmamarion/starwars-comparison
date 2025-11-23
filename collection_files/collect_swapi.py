import requests
import sqlite3
import json
import os

# NOTE:
# There are 76 vehicles and 75 starships in swapi. We're treating them both as "vehicles"
# and storing them in one table with over over 100 rows, which satisfies the
# "Access and store at least 100 rows in your database from each API/website" requirement

# Vehicles and manufacturers each get their own seperate tables in the database, which satisfies the
# "For at least one API you must have two tables" requirement.

# The vehicle table contains a foriegn key from the manufacturer table, which satisfies the
# "For at least one API you must have two tables that share an integer key" requirement.


def get_vehicle_data(type="vehicle", request_id=1):
    """
    creates an API request to the swapi and retreieves information for a SINGLE entry

    ARGUMENTS:
        type (string): specifies the type of request, either "starship" or "vehicle"
        request_id (int): the id of the vehicle
    RETURNS:
        data (dict): json dictionary of requested data
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

        # Check if the request was actually successful
        if response.status_code != 200:
            # If ID doesn't exist, return None so the loop can skip it
            return None

        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching API data: {e}")
        exit()


def update_vehicle_table(data, database_filename):
    """
    Adds vehicle data for a SINGLE vehicle to the specified database in the "vehicles" table.

    ARGUMENTS:
        data (dict): json data for a vehicle
        database_filename (string): filename of the target database
    RETURNS:
        None
    """

    # Connect to SQLite database
    conn = sqlite3.connect(database_filename)
    cursor = conn.cursor()

    # ======= NAME =======
    vehicle_name = data.get("name")

    # ======= LENGTH =======
    # Handle "unknown" and commas in numbers (e.g., "1,250")
    raw_length = data.get("length", "0")

    # Remove commas and check if it is a digit (handles "unknown")
    clean_length = str(raw_length).replace(",", "")
    if clean_length.replace(".", "", 1).isdigit():
        vehicle_length = int(float(clean_length))

    # ======= ID =======
    # URLs look like: https://swapi.info/api/vehicles/4/
    # Splitting by '/' and taking the second to last item
    url_parts = data.get("url", "").split("/")
    # Filter out empty strings to handle trailing slashes safely
    url_parts = [p for p in url_parts if p]
    vehicle_id = int(url_parts[-1])

    # Uses INSERT OR IGNORE to prevent crashing if script is run twice
    cursor.execute(
        """INSERT OR IGNORE INTO vehicles (id, name, vehicle_length) VALUES (?, ?, ?)""",
        (vehicle_id, vehicle_name, vehicle_length),
    )
    conn.commit()
    conn.close()


def get_manufacturer_data(database_filename):
    """
    Iterates through vehicle IDs to find manufacturers.

    ARGUMENTS:
        database_filename (string): filename of the target database
    RETURNS:
        manufacturer_list (list): List of manufacturers.
    """
    cache_filename = "swapi_manufacturers.json"

    # Check if cache exists
    if os.path.exists(cache_filename):
        print(f"Loading manufacturers from cache: {cache_filename}")
        with open(cache_filename, "r") as f:
            manufacturer_list = json.load(f)
        return manufacturer_list

    # If no cache, fetch from API
    manufacturer_list = []
    api_types = ["vehicle", "starship"]

    # Iterate through the types
    for search_type in api_types:
        print(f"scanning {search_type}s")

        # Iterate through IDs
        for i in range(1, 77):
            vehicle_data = get_vehicle_data(search_type, i)

            # if getting data was successful
            if vehicle_data:

                # Grab the manufacturer
                vehicle_manufacturer = vehicle_data.get("manufacturer")

                # Check if the manufacturer exists and isn't "unknown"
                if vehicle_manufacturer and vehicle_manufacturer != "unknown":

                    # Split the string by comma
                    # "Incom, Subpro" becomes ["Incom", " Subpro"]
                    split_names = vehicle_manufacturer.split(",")

                    for name in split_names:
                        # 2. Strip whitespace
                        # " Subpro" becomes "Subpro"
                        clean_name = name.strip()

                        if clean_name not in manufacturer_list:
                            manufacturer_list.append(clean_name)
                            print(f"Found: {clean_name}")

    # Save the result to a JSON file for next time
    try:
        with open(cache_filename, "w") as f:
            json.dump(manufacturer_list, f)
        print(f"Saved data to cache: {cache_filename}")
    except IOError as e:
        print(f"Warning: Could not save cache file: {e}")

    return manufacturer_list


def update_manufacturer_table(manufacturer_list, database_filename, limit=25):
    """
    Takes a list of manufacturer names and inserts them into the database.
    Ignores duplicates automatically.

    ARGUMENTS:
        manufacturer_list (list): List of strings (e.g., ["Incom", "Kuat"])
        database_filename (str): The database file
    """
    # Connect to SQLite database
    conn = sqlite3.connect(database_filename)
    cursor = conn.cursor()

    # Initalize variables
    newly_added_count = 0

    for name in manufacturer_list:
        # Check if limit has been hit
        if newly_added_count >= limit:
            print(f"Limit of {limit} new entries reached. Stopping")
            break

        # Check if the manufacturer already exists
        cursor.execute("SELECT id FROM manufacturers WHERE name = ?", (name,))
        result = cursor.fetchone()

        if not result:
            # Insert the new manufacturer
            cursor.execute("INSERT INTO manufacturers (name) VALUES (?)", (name,))
            conn.commit()  # Commit immediately or at the end

            newly_added_count += 1
            print(f"Added new manufacturer: {name}")

    # Save changes
    conn.commit()
    conn.close()

    if newly_added_count == 0:
        print("NO NEW MANUFACTURERS WERE ADDED")
    else:
        print("Manufacturer table updated.")


# For debugging
def test():
    print(get_manufacturer_data("starwars.db"))


if __name__ == "__main__":
    test()
