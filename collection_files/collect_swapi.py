import requests
import sqlite3
import cache


# NOTE:
# There are 76 vehicles and 75 starships in swapi. We're treating them both as "vehicles"
# and storing them in one table with over over 100 rows, which satisfies the
# "Access and store at least 100 rows in your database from each API/website" requirement

# Vehicles and manufacturers each get their own seperate tables in the database, which satisfies the
# "For at least one API you must have two tables" requirement.

# The vehicle table contains a foriegn key from the manufacturer table, which satisfies the
# "For at least one API you must have two tables that share an integer key" requirement.


def fetch_and_cache_data():
    # These are fragments that appear after splitting eg "Company, Inc."
    skip_list = [
        "inc",
        "inc.",
        "ltd",
        "ltd.",
        "corporation",
        "incorporated",
        "co.",
        "co",
        "unknown",
    ]

    cache_filename = "api_caches/swapi_full_data.json"

    # Check if cache already exists
    cached_data = cache.load_cache(cache_filename)
    if cached_data:
        print(f"Loaded {len(cached_data)} items from cache.")
        return cached_data

    print("Fetching new data from API...")
    all_items = []
    api_types = ["vehicle", "starship"]
    max_id_range = 80  # Adjust if you want more (there are ~75 of each)

    for search_type in api_types:
        base_url = (
            "https://swapi.info/api/starships/"
            if search_type == "starship"
            else "https://swapi.info/api/vehicles/"
        )

        for i in range(1, max_id_range):
            try:
                response = requests.get(base_url + str(i))
                if response.status_code != 200:  # if the call was successful
                    continue

                raw_data = response.json()

                # --- CLEANING DATA (Before Caching) ---

                # Clean ID
                url_parts = raw_data.get("url", "").split("/")
                clean_id = int([p for p in url_parts if p][-1])

                # Clean Length
                raw_length = raw_data.get("length", "0")
                clean_length = str(raw_length).replace(",", "")
                if clean_length.replace(".", "", 1).isdigit():
                    final_length = int(float(clean_length))
                else:
                    final_length = 0

                # Clean manufacturer
                manufacturer_list = []
                raw_man = raw_data.get("manufacturer", "")
                if raw_man and raw_man != "unknown":
                    # Replace slash with comma so it splits correctly
                    normalized = raw_man.replace("/", ",")
                    split_names = normalized.split(",")

                    for name in split_names:
                        c_name = name.strip().title()
                        if c_name.lower() not in skip_list and len(c_name) > 1:
                            if c_name == "Cyngus Spaceworks":
                                c_name = "Cygnus Spaceworks"
                            manufacturer_list.append(c_name)

                clean_obj = {
                    "id": clean_id,
                    "category": search_type,
                    "name": raw_data.get("name"),
                    "length": final_length,
                    "manufacturers": manufacturer_list,  # List of strings
                    "cost_in_credits": raw_data.get("cost_in_credits"),
                }

                all_items.append(clean_obj)
                print(f"Fetched: {clean_obj['name']}")

            except Exception as e:
                print(f"Error fetching ID {i}: {e}")

    # Save to cache
    cache.save_cache(all_items, cache_filename)
    return all_items


def seed_manufacturers(data_list, database_filename, limit=25):
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

    print(f"\nScanning manufacturers for insertion (Limit: {limit})...")

    for item in data_list:
        if newly_added_count >= limit:
            print(f"Limit of {limit} reached for MANUFACTURERS.")
            break
        for name in item["manufacturers"]:
            # Check if limit has been hit for this run
            if newly_added_count >= limit:
                print(f"Limit of {limit} reached for MANUFACTURERS.")
                break

            # Check if the manufacturer already exists
            cursor.execute("SELECT id FROM manufacturers WHERE name = ?", (name,))
            result = cursor.fetchone()

            if not result:
                # Insert the new manufacturer
                cursor.execute("INSERT INTO manufacturers (name) VALUES (?)", (name,))
                newly_added_count += 1
                print(f"Added new manufacturer: {name}")

    # Save changes
    conn.commit()
    conn.close()

    if newly_added_count == 0:
        print("No new manufacturers added (they might all be in the DB already).")
    else:
        print(f"{newly_added_count} manufacturers added.")


def seed_vehicles(data_list, database_filename, limit=25):
    conn = sqlite3.connect(database_filename)
    cursor = conn.cursor()

    newly_added_count = 0

    print(f"\nScanning {len(data_list)} vehicles for insertion...")

    for item in data_list:
        if newly_added_count >= limit:
            print(f"Limit of {limit} reached for VEHICLES.")
            break

        # Check if vehicle already exists
        cursor.execute("SELECT id FROM vehicles WHERE id = ?", (item["id"],))
        if cursor.fetchone():
            continue  # Skip if exists

        # Find Manufacturer ID
        # (Take the first one in the list as the primary manufacturer)
        man_id = None
        if item["manufacturers"]:
            primary_man_name = item["manufacturers"][0]
            cursor.execute(
                "SELECT id FROM manufacturers WHERE name = ?", (primary_man_name,)
            )
            res = cursor.fetchone()
            if res:
                man_id = res[0]

        # Insert
        cursor.execute(
            "INSERT INTO vehicles (swapi_id, name, length, manufacturer_id) VALUES (?, ?, ?, ?)",
            (item["id"], item["name"], item["length"], man_id),
        )
        print(f" + Added Vehicle: {item['name']}")
        newly_added_count += 1

    if newly_added_count == 0:
        print("No new vehicles added (they might all be in the DB already).")
    else:
        print(f"{newly_added_count} vehicles added.")

    conn.commit()
    conn.close()
    return newly_added_count
