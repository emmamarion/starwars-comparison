from bs4 import BeautifulSoup
import requests
import re
import sqlite3


def collect_comics():
    """

    RETURNS:
        html_content
    """
    url = "https://starwars.fandom.com/wiki/Timeline_of_canon_media"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises error for 404, 500, etc.
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        exit()


def scrape(html_content, limit=25):
    soup = BeautifulSoup(html_content, "html.parser")
    comic_table_rows = soup.find_all("tr", class_="comic")

    conn = sqlite3.connect("starwars.db")
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

        date_text = cells[3].get_text(strip=True)

        try:
            cursor.execute(
                "INSERT INTO comics (title, release_date) VALUES (?, ?)",
                (title, date_text),
            )
            conn.commit()
            rows_added += 1
            print(f"Added: {title}")
        except sqlite3.IntegrityError:
            # if the title is already in the database, skip it
            continue

    conn.close()
    return rows_added


def main():
    html_content = collect_comics()
    total_added = scrape(html_content)
    print(f"Job complete. Total new comics added: {total_added}")


if __name__ == "__main__":
    main()
