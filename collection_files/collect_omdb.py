import requests
import sqlite3

import re


def get_api_key(filename="api_keys.txt"):
    """
    Returns the Api Key for the OMDB API.

    Args:
        filename (str, optinial): filename of textfile where api keys are stored

    Returns:
        api_key (str):
    """
    api_key = None
    try:
        with open(filename, "r") as f:
            text_file_contents = f.read().strip()
            api_key = re.search(r"omdb: (.*)", text_file_contents)
            if api_key:
                api_key = api_key.group(1)
                print("API KEY LOADED")
            else:
                print("WARNING: API key is not loaded.")

    except FileNotFoundError:
        print(f"ERROR: file: {filename} not found.")

    return api_key


def collect_omdb_data():
    """
    Collects Star Wars movie data from OMDB API.
    
    Returns:
        list: List of movie dictionaries with parsed data
    """
    # Get API key
    api_key = get_api_key()
    if not api_key:
        return []
    
    # List of Star Wars movie IMDb IDs
    movie_ids = [
        ("tt0076759", "Star Wars: Episode IV - A New Hope"),
        ("tt0080684", "Star Wars: Episode V - The Empire Strikes Back"),
        ("tt0086190", "Star Wars: Episode VI - Return of the Jedi"),
        ("tt0120915", "Star Wars: Episode I - The Phantom Menace"),
        ("tt0121765", "Star Wars: Episode II - Attack of the Clones"),
        ("tt0121766", "Star Wars: Episode III - Revenge of the Sith"),
        ("tt2488496", "Star Wars: Episode VII - The Force Awakens"),
        ("tt2527336", "Star Wars: Episode VIII - The Last Jedi"),
        ("tt2527338", "Star Wars: Episode IX - The Rise of Skywalker"),
        ("tt3748528", "Rogue One: A Star Wars Story"),
        ("tt3778644", "Solo: A Star Wars Story"),
    ]
    
    movies_data = []
    base_url = "http://www.omdbapi.com/"
    
    for imdb_id, title in movie_ids:
        params = {
            "apikey": api_key,
            "i": imdb_id,
            "type": "movie"
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("Response") == "True":
                # Parse box office (remove $ and commas)
                box_office = None
                if data.get("BoxOffice") and data.get("BoxOffice") != "N/A":
                    box_office_str = data.get("BoxOffice").replace("$", "").replace(",", "")
                    try:
                        box_office = int(box_office_str)
                    except ValueError:
                        pass
                
                # Parse IMDb rating
                imdb_rating = None
                if data.get("imdbRating") and data.get("imdbRating") != "N/A":
                    try:
                        imdb_rating = float(data.get("imdbRating"))
                    except ValueError:
                        pass
                
                # Parse Rotten Tomatoes score
                rotten_tomatoes = None
                ratings_list = data.get("Ratings", [])
                for rating in ratings_list:
                    if rating.get("Source") == "Rotten Tomatoes":
                        rt_str = rating.get("Value", "")
                        if "%" in rt_str:
                            try:
                                rotten_tomatoes = int(rt_str.replace("%", ""))
                            except ValueError:
                                pass
                
                movie_info = {
                    "imdb_id": data.get("imdbID"),
                    "title": data.get("Title"),
                    "box_office": box_office,
                    "imdb_rating": imdb_rating,
                    "rotten_tomatoes": rotten_tomatoes
                }
                movies_data.append(movie_info)
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {title}: {e}")
    
    return movies_data



def insert_into_database(limit=25):
    pass


if __name__ == "__main__":
    API_KEY = get_api_key()
    print(API_KEY)
