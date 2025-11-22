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

    # Table 1: SWAPI vehicle table
    table_1 = """
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            legnth INTEGER,
            cost_in_credits INTEGER
            manufacturer INTEGER
        )
    """

    # Table 2: manufacturer
    table_2 = """
        CREATE TABLE IF NOT EXISTS manufacturers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """

    # Table 5: Media types
    table_5 = """
        CREATE TABLE IF NOT EXISTS media_types (
            id INTEGER PRIMARY KEY,
            media_type TEXT
        )
    """

    cursor.execute(table_1)
    cursor.execute(table_2)
    cursor.execute(table_5)

    conn.commit()  # save the changes
    conn.close()  # close the connection
