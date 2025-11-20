import sqlite3


def database_setup():
    conn = sqlite3.connect("starwars.db")
    cursor = conn.cursor()

    table1 = """
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    
    """

    cursor.execute(table1)

    conn.commit()  # save the changes
    conn.close()  # close the connection


database_setup()
