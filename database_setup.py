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

    # Table 5: Media types
    table_5 = """
        CREATE TABLE IF NOT EXISTS comics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            release_date INTEGER
        )
    """
    # Parent tables
    cursor.execute(table_5)  # Create Comic Table

    conn.commit()  # save the changes
    conn.close()  # close the connection
    print("Database setup complete")
