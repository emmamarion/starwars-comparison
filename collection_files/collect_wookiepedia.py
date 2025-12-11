from bs4 import BeautifulSoup
import requests
import sqlite3


def collect_comics():
    """
    Fetches the raw HTML content from the Wookieepedia timeline page using a GET request.

    The function includes error handling: it raises an exception for bad HTTP
    status codes (4xx, 5xx) and exits the program if a network error occurs.

    Args:
        None

    Returns:
        str: The raw HTML content of the Wookieepedia 'Timeline of canon media' page.
    """
    url = "https://starwars.fandom.com/wiki/Timeline_of_canon_media"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises error for 404, 500, etc.
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        exit()


def scrape(html_content, database_filename="starwars.db", limit=25):
    """
    Scrapes Star Wars comic data from an HTML page, extracts the title and release
    year, and inserts them into the 'comics' table in the SQLite database.

    The function limits the total number of new items added to prevent exceeding
    the project's 25-item-per-run limit.
    It also handles duplicate entries by skipping comics whose title already exists
    in the database.

    Args:
        html_content (str): The raw HTML content from the Wookieepedia timeline page.
        database_filename (str): The string of the database filename.
        limit (int, optional): The maximum number of new comic rows to add during this function call. Defaults to 25.

    Returns:
        int: The number of new comic rows successfully added to the database.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    comic_table_rows = soup.find_all("tr", class_="comic")

    conn = sqlite3.connect(database_filename)
    cursor = conn.cursor()
    rows_added = 0

    print(f"Found {len(comic_table_rows)} comic rows. Processing...")

    for table_row in comic_table_rows:
        if rows_added >= limit:
            print("Reached limit of 25 rows.")
            break

        cells = table_row.find_all("td")
        title_cell = cells[2]
        for unordered_list in title_cell.find_all("ul"):
            unordered_list.decompose()

        title = title_cell.get_text(strip=True)
        title = title.strip("†")

        # Change date to year to avoid duplicate string data
        date_text = cells[3].get_text(strip=True)
        year = date_text[:4]

        try:
            cursor.execute(
                "INSERT INTO comics (title, release_date) VALUES (?, ?)",
                (title, year),
            )
            conn.commit()
            rows_added += 1
            print(f"Added: {title}")
        except sqlite3.IntegrityError:
            # if the title is already in the database, skip it
            continue

    conn.close()
    return rows_added


if __name__ == "__main__":
    html_content = collect_comics()
    scrape(html_content)
