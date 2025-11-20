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

    # Table 1: character table
    table_1 = """
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            height INTEGER,
            homeworld_id INTEGER
        )
    """

    # Table 2: planet table
    table_2 = """
        CREATE TABLE IF NOT EXISTS planets (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            population INTEGER
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
