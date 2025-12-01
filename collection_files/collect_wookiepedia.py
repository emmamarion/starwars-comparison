from bs4 import BeautifulSoup
import requests
import re


def collect_comics():
    """

    RETURNS:
        html_content
    """
    url = "https://starwars.fandom.com/wiki/Timeline_of_canon_media"
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        return html_content
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        exit()


def scrape(html_content):
    extratced_data = []

    soup = BeautifulSoup(html_content, "html.parser")
    comic_table_rows = soup.find_all("tr", class_="comic")
    for table_row in comic_table_rows:
        cells = table_row.find_all("td")

        cells[3]


def main():
    html_content = collect_comics()
    print(scrape(html_content))


if __name__ == "__main__":
    main()
