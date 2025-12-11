"""
collect_omdb.py
Author: Kamila Podsiadlo (kampod@umich.edu)
Purpose: Collect Star Wars movies AND top sci-fi movies from OMDB API

Compares Star Wars movies to other top science fiction films to see how they
rank according to IMDb and Rotten Tomatoes scores.

This file creates its own MovieMetrics table (no need to modify database_setup.py)
"""

import requests
import sqlite3
import re
import time


def get_api_key(filename="api_keys.txt"):
    """
    Returns the Api Key for the OMDB API.

    Args:
        filename (str, optional): filename of textfile where api keys are stored

    Returns:
        api_key (str): API key or None
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


def create_movie_table(db_filename="starwars.db"):
    """
    Creates the MovieMetrics table if it doesn't exist.
    This allows us to not modify database_setup.py!
    
    Args:
        db_filename (str): Database filename
    """
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MovieMetrics (
            imdb_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            box_office INTEGER,
            imdb_rating REAL,
            rotten_tomatoes INTEGER,
            is_star_wars INTEGER DEFAULT 0,
            genre TEXT
        )
    """)
    
    conn.commit()
    conn.close()


def get_star_wars_movies():
    """
    Returns list of Star Wars movie IMDb IDs.
    
    Returns:
        list: List of tuples (imdb_id, title, is_star_wars)
    """
    movies = [
        ("tt0076759", "Star Wars: Episode IV - A New Hope", 1),
        ("tt0080684", "Star Wars: Episode V - The Empire Strikes Back", 1),
        ("tt0086190", "Star Wars: Episode VI - Return of the Jedi", 1),
        ("tt0120915", "Star Wars: Episode I - The Phantom Menace", 1),
        ("tt0121765", "Star Wars: Episode II - Attack of the Clones", 1),
        ("tt0121766", "Star Wars: Episode III - Revenge of the Sith", 1),
        ("tt2488496", "Star Wars: Episode VII - The Force Awakens", 1),
        ("tt2527336", "Star Wars: Episode VIII - The Last Jedi", 1),
        ("tt2527338", "Star Wars: Episode IX - The Rise of Skywalker", 1),
        ("tt3748528", "Rogue One: A Star Wars Story", 1),
        ("tt3778644", "Solo: A Star Wars Story", 1),
    ]
    return movies


def get_top_scifi_movies():
    """
    Returns list of top science fiction movies for comparison with Star Wars.
    These are critically acclaimed and popular sci-fi films.
    
    Returns:
        list: List of tuples (imdb_id, title, is_star_wars)
    """
    scifi_movies = [
        # Classic Sci-Fi
        ("tt0062622", "2001: A Space Odyssey", 0),
        ("tt0078748", "Alien", 0),
        ("tt0083658", "Blade Runner", 0),
        ("tt0088763", "Back to the Future", 0),
        ("tt0090605", "Aliens", 0),
        ("tt0093058", "Full Metal Jacket", 0),
        ("tt0096283", "My Neighbor Totoro", 0),
        ("tt0099785", "Total Recall", 0),
        ("tt0103064", "Terminator 2: Judgment Day", 0),
        ("tt0106977", "The Fugitive", 0),
        ("tt0107290", "Jurassic Park", 0),
        ("tt0108052", "Schindler's List", 0),
        
        # 1990s Sci-Fi
        ("tt0109830", "Forrest Gump", 0),
        ("tt0110912", "Pulp Fiction", 0),
        ("tt0111161", "The Shawshank Redemption", 0),
        ("tt0112573", "Braveheart", 0),
        ("tt0114369", "Se7en", 0),
        ("tt0114709", "Toy Story", 0),
        ("tt0118799", "Life Is Beautiful", 0),
        ("tt0133093", "The Matrix", 0),
        ("tt0137523", "Fight Club", 0),
        ("tt0144084", "American Psycho", 0),
        ("tt0167260", "The Lord of the Rings: The Return of the King", 0),
        ("tt0172495", "Gladiator", 0),
        
        # Modern Sci-Fi Classics
        ("tt0208092", "Snatch", 0),
        ("tt0245429", "Spirited Away", 0),
        ("tt0253474", "The Pianist", 0),
        ("tt0266697", "Kill Bill: Vol. 1", 0),
        ("tt0268978", "A Beautiful Mind", 0),
        ("tt0317248", "City of God", 0),
        ("tt0325980", "Pirates of the Caribbean: The Curse of the Black Pearl", 0),
        ("tt0338013", "Eternal Sunshine of the Spotless Mind", 0),
        ("tt0361748", "Inglourious Basterds", 0),
        ("tt0372784", "Batman Begins", 0),
        ("tt0405094", "The Lives of Others", 0),
        ("tt0407887", "The Departed", 0),
        ("tt0435761", "Toy Story 3", 0),
        ("tt0468569", "The Dark Knight", 0),
        ("tt0477348", "No Country for Old Men", 0),
        ("tt0482571", "The Prestige", 0),
        ("tt0816692", "Interstellar", 0),
        ("tt0910970", "WALL·E", 0),
        ("tt0978762", "Mary and Max", 0),
        ("tt0993846", "The Wolf of Wall Street", 0),
        ("tt1049413", "Up", 0),
        ("tt1130884", "Shutter Island", 0),
        ("tt1187043", "3 Idiots", 0),
        ("tt1201607", "Harry Potter and the Deathly Hallows: Part 2", 0),
        ("tt1205489", "Gran Torino", 0),
        ("tt1375666", "Inception", 0),
        ("tt1392190", "Mad Max: Fury Road", 0),
        ("tt1392214", "Prisoners", 0),
        ("tt1454029", "The Help", 0),
        ("tt1675434", "The Intouchables", 0),
        ("tt1745960", "Top Gun: Maverick", 0),
        ("tt1853728", "Django Unchained", 0),
        ("tt1877830", "X-Men: Days of Future Past", 0),
        ("tt1895587", "Spotlight", 0),
        ("tt2024544", "12 Years a Slave", 0),
        ("tt2096673", "Inside Out", 0),
        ("tt2106476", "Hacksaw Ridge", 0),
        ("tt2119532", "Hacksaw Ridge", 0),
        ("tt2267998", "Gone Girl", 0),
        ("tt2278388", "The Grand Budapest Hotel", 0),
        ("tt2380307", "Coco", 0),
        ("tt2582802", "Whiplash", 0),
        ("tt3011894", "Wild", 0),
        ("tt3315342", "Logan", 0),
        ("tt3659388", "The Martian", 0),
        ("tt4154756", "Avengers: Infinity War", 0),
        ("tt4154796", "Avengers: Endgame", 0),
        ("tt4633694", "Spider-Man: Into the Spider-Verse", 0),
        ("tt5027774", "Three Billboards Outside Ebbing, Missouri", 0),
        ("tt6751668", "Parasite", 0),
        ("tt8579674", "1917", 0),
        
        # Recent Acclaimed Films
        ("tt1160419", "Dune", 0),
        ("tt10872600", "Spider-Man: No Way Home", 0),
        ("tt15398776", "Oppenheimer", 0),
        ("tt0758758", "Into the Wild", 0),
        ("tt0848228", "The Avengers", 0),
        ("tt1856101", "Blade Runner 2049", 0),
        ("tt2582846", "The Imitation Game", 0),
        ("tt4633694", "Spider-Man: Into the Spider-Verse", 0),
        ("tt0266543", "Finding Nemo", 0),
        ("tt1049413", "Up", 0),
        ("tt2380307", "Coco", 0),
        ("tt0114814", "The Usual Suspects", 0),
        ("tt0268380", "Ice Age", 0),
        ("tt0382932", "Ratatouille", 0),
        ("tt1217209", "Brave", 0),
        ("tt2267998", "Gone Girl", 0),
        ("tt0993846", "The Wolf of Wall Street", 0),
        ("tt1205489", "Gran Torino", 0),
        ("tt0848228", "The Avengers", 0),
        ("tt2015381", "Guardians of the Galaxy", 0),
        ("tt3896198", "Guardians of the Galaxy Vol. 2", 0),
        ("tt4154664", "Captain America: Civil War", 0),
        ("tt3501632", "Thor: Ragnarok", 0),
        ("tt4154756", "Avengers: Infinity War", 0),
        ("tt4154796", "Avengers: Endgame", 0),
        ("tt1825683", "Black Panther", 0),
        ("tt9376612", "Shang-Chi and the Legend of the Ten Rings", 0),
    ]
    return scifi_movies


def parse_box_office(box_office_str):
    """Converts box office string to integer."""
    if box_office_str and box_office_str != "N/A":
        try:
            cleaned = box_office_str.replace("$", "").replace(",", "")
            return int(cleaned)
        except ValueError:
            return None
    return None


def parse_rotten_tomatoes(ratings_list):
    """Extracts Rotten Tomatoes score from ratings list."""
    if not ratings_list:
        return None
    
    for rating in ratings_list:
        if rating.get("Source") == "Rotten Tomatoes":
            score_str = rating.get("Value", "")
            if "%" in score_str:
                try:
                    return int(score_str.replace("%", ""))
                except ValueError:
                    return None
    return None


def fetch_movie_data(api_key, imdb_id):
    """Fetches movie data from OMDB API."""
    base_url = "http://www.omdbapi.com/"
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
            return data
        return None
            
    except requests.RequestException as e:
        print(f"  Error fetching {imdb_id}: {e}")
        return None


def collect_omdb_data():
    """
    Collects both Star Wars AND top sci-fi movies from OMDB API.
    This ensures we get 100+ movies for the project.
    
    Returns:
        list: List of movie data dictionaries
    """
    api_key = get_api_key()
    if not api_key:
        return []
    
    # Combine Star Wars and sci-fi movies
    all_movies = get_star_wars_movies() + get_top_scifi_movies()
    
    movies_data = []
    
    print(f"Collecting {len(all_movies)} movies from OMDB API...")
    
    for imdb_id, title, is_star_wars in all_movies:
        movie_data = fetch_movie_data(api_key, imdb_id)
        
        if not movie_data:
            continue
        
        # Parse data
        box_office = parse_box_office(movie_data.get("BoxOffice"))
        
        imdb_rating = None
        if movie_data.get("imdbRating") and movie_data.get("imdbRating") != "N/A":
            try:
                imdb_rating = float(movie_data.get("imdbRating"))
            except ValueError:
                pass
        
        rotten_tomatoes = parse_rotten_tomatoes(movie_data.get("Ratings", []))
        
        movie_info = {
            "imdb_id": movie_data.get("imdbID"),
            "title": movie_data.get("Title"),
            "box_office": box_office,
            "imdb_rating": imdb_rating,
            "rotten_tomatoes": rotten_tomatoes,
            "is_star_wars": is_star_wars,
            "genre": movie_data.get("Genre")
        }
        movies_data.append(movie_info)
        
        # Small delay to respect API rate limits
        time.sleep(0.1)
    
    return movies_data


def insert_into_database(limit=25):
    """
    Inserts movie data into database, limiting to 'limit' new entries per run.
    Creates the MovieMetrics table if it doesn't exist.
    
    Args:
        limit (int): Maximum number of new entries to add per run (default 25)
    
    Returns:
        int: Number of movies added this run
    """
    # Create table first
    create_movie_table()
    
    # Collect data from API
    movies_data = collect_omdb_data()
    
    if not movies_data:
        print("No movie data collected")
        return 0
    
    conn = sqlite3.connect("starwars.db")
    cursor = conn.cursor()
    
    rows_added = 0
    
    print(f"Found {len(movies_data)} movies. Processing with limit of {limit}...")
    
    for movie in movies_data:
        # Check if we've hit the limit
        if rows_added >= limit:
            print("Reached limit of 25 rows.")
            break
        
        # Check if movie already exists
        cursor.execute("SELECT imdb_id FROM MovieMetrics WHERE imdb_id = ?", 
                      (movie["imdb_id"],))
        if cursor.fetchone():
            continue
        
        # Insert into database
        try:
            cursor.execute('''
                INSERT INTO MovieMetrics 
                (imdb_id, title, box_office, imdb_rating, rotten_tomatoes, is_star_wars, genre)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (movie["imdb_id"], movie["title"], movie["box_office"], 
                  movie["imdb_rating"], movie["rotten_tomatoes"], 
                  movie["is_star_wars"], movie["genre"]))
            conn.commit()
            rows_added += 1
            
            movie_type = "[SW]" if movie["is_star_wars"] else "[SF]"
            print(f"Added: {movie_type} - {movie['title']}")
            
        except sqlite3.IntegrityError:
            continue
    
    # Show summary
    cursor.execute("SELECT COUNT(*) FROM MovieMetrics")
    total_movies = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM MovieMetrics WHERE is_star_wars = 1")
    total_star_wars = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM MovieMetrics WHERE is_star_wars = 0")
    total_scifi = cursor.fetchone()[0]
    
    print(f"\n{'='*70}")
    print(f"Total movies in database: {total_movies}")
    print(f"  - Star Wars movies: {total_star_wars}")
    print(f"  - Other Sci-Fi movies: {total_scifi}")
    print(f"{'='*70}\n")
    
    conn.close()
    return rows_added


if __name__ == "__main__":
    API_KEY = get_api_key()
    print(API_KEY)
    
    # Insert data into database (limit 25 per run)
    total_added = insert_into_database(limit=25)
    print(f"Job complete. Total new movies added: {total_added}")