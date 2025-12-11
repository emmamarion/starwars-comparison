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

    table_1 = """
        CREATE TABLE IF NOT EXISTS lego_themes (
            id   INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
    """

    table_2 = """
        CREATE TABLE IF NOT EXISTS lego_sets (
            set_num   TEXT PRIMARY KEY,
            name      TEXT NOT NULL,
            year      INTEGER,
            num_parts INTEGER,
            theme_id  INTEGER,
            FOREIGN KEY(theme_id) REFERENCES lego_themes(id)
        )
    """

    table_3 = """
         CREATE TABLE IF NOT EXISTS MovieMetrics (
            imdb_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            box_office INTEGER,
            imdb_rating REAL,
            rotten_tomatoes INTEGER,
            is_star_wars INTEGER DEFAULT 0,
            genre TEXT
        )   
    """

    # Table 5: Media types
    table_5 = """
        CREATE TABLE IF NOT EXISTS comics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            release_date INTEGER
        )
    """
    # Parent tables
    cursor.execute(table_1)
    cursor.execute(table_2)
    cursor.execute(table_3)
    cursor.execute(table_5)  # Create Comic Table

    conn.commit()  # save the changes
    conn.close()  # close the connection
    print("Database setup complete")


if __name__ == "__main__":
    database_setup(filename="starwars.db")
