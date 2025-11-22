import sqlite3


def database_setup(filename):
    """
    Generates database if it doesn't exist and then creates all tables.

    ARGS:
        filename (str): filename of the database to create

    RETURNS:
        None
    """
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    # Table 1: SWAPI manufacturer table (Parent table)
    table_1 = """
        CREATE TABLE IF NOT EXISTS manufacturers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """

    # Table 2: SWAPI vehicle data (Child table)
    table_2 = """
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY,
            name TEXT,
            length INTEGER, 
            cost_in_credits INTEGER,
            manufacturer_id INTEGER,
            FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id)
        )
    """

    # Table 5: Media types
    table_5 = """
        CREATE TABLE IF NOT EXISTS media_types (
            id INTEGER PRIMARY KEY,
            media_type TEXT
        )
    """
    # Parent tables
    cursor.execute(table_1)  # Create Manufacturers
    cursor.execute(table_5)  # Create Media Types

    # Child tables
    cursor.execute(table_2)  # Creat Vehicles

    conn.commit()  # save the changes
    conn.close()  # close the connection
    print("Database setup complete")
