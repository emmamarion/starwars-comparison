import sqlite3


def calculate_comics_per_year(db_filename="starwars.db"):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    query = """
    SELECT release_date, COUNT(*)
    FROM comics
    GROUP BY release_date
    ORDER BY release_date ASC
    """

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        comics_by_year = {year: count for year, count in results}
        return comics_by_year

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return {}

    finally:
        conn.close()


def write_comic_data(data, filename="calculation_results.txt"):
    """
    Writes the calculated data to a text file in a human-readable format.
    """
    try:
        with open(filename, "w") as f:
            f.write("Star Wars Comics Released Per Year\n")
            f.write("================================\n")
            # Iterate through the dictionary to write clear lines
            for year, count in data.items():
                f.write(f"Year: {year} | Comics Released: {count}\n")

        print(f"Successfully wrote formatted results to {filename}")
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")


if __name__ == "__main__":
    data = calculate_comics_per_year()
    print("Comics per year", data)
    write_comic_data(data)
