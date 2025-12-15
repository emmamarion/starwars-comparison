import sqlite3


def calculate_comics_per_year(db_filename="starwars.db"):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    query = """
    SELECT release_date, COUNT(*)
    FROM comics
    WHERE release_date != '' AND release_date IS NOT NULL
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


# ============================================================================
# OMDB CALCULATIONS - Kamila Podsiadlo (kampod@umich.edu)
# Compares Star Wars movies to all other collected top movies
# ============================================================================


def calculate_rating_differences(db_filename="starwars.db"):
    """
    REQUIRED CALCULATION: Difference between IMDb and RT for all movies.
    This shows which movies have bigger disagreement between critics and audiences.

    Returns:
        dict: All movies with their rating differences
    """
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    query = """
    SELECT title, imdb_rating, rotten_tomatoes, is_star_wars
    FROM MovieMetrics
    WHERE imdb_rating IS NOT NULL AND rotten_tomatoes IS NOT NULL
    ORDER BY title ASC
    """

    try:
        cursor.execute(query)
        results = cursor.fetchall()

        rating_diffs = {}
        for title, imdb_rating, rt_score, is_star_wars in results:
            imdb_normalized = imdb_rating * 10
            difference = imdb_normalized - rt_score
            rating_diffs[title] = {
                "imdb": imdb_normalized,
                "rt": rt_score,
                "difference": difference,
                "is_star_wars": is_star_wars,
            }

        return rating_diffs

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return {}

    finally:
        conn.close()


def calculate_average_ratings_comparison(db_filename="starwars.db"):
    """
    REQUIRED CALCULATION: Compare Star Wars average ratings to all other top movies.
    This answers: Do Star Wars movies rate higher or lower than other top films?

    Returns:
        dict: Averages for Star Wars vs Other Top Movies
    """
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    try:
        # Star Wars averages
        cursor.execute(
            """
            SELECT AVG(imdb_rating), AVG(rotten_tomatoes), COUNT(*)
            FROM MovieMetrics
            WHERE is_star_wars = 1 
            AND imdb_rating IS NOT NULL 
            AND rotten_tomatoes IS NOT NULL
        """
        )
        sw_result = cursor.fetchone()
        sw_imdb = sw_result[0] * 10 if sw_result[0] else 0
        sw_rt = sw_result[1] if sw_result[1] else 0
        sw_count = sw_result[2]

        # Other movies averages
        cursor.execute(
            """
            SELECT AVG(imdb_rating), AVG(rotten_tomatoes), COUNT(*)
            FROM MovieMetrics
            WHERE is_star_wars = 0 
            AND imdb_rating IS NOT NULL 
            AND rotten_tomatoes IS NOT NULL
        """
        )
        other_result = cursor.fetchone()
        other_imdb = other_result[0] * 10 if other_result[0] else 0
        other_rt = other_result[1] if other_result[1] else 0
        other_count = other_result[2]

        return {
            "star_wars": {"imdb": sw_imdb, "rt": sw_rt, "count": sw_count},
            "other_movies": {"imdb": other_imdb, "rt": other_rt, "count": other_count},
        }

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return {}

    finally:
        conn.close()


def calculate_top_rated_movies(db_filename="starwars.db"):
    """
    EXTRA CALCULATION: Find top 10 movies overall and see where Star Wars ranks.
    This shows if any Star Wars movies are among the highest rated.

    Returns:
        dict: Top movies by IMDb and RT, with Star Wars highlighted
    """
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    try:
        # Top 10 by IMDb
        cursor.execute(
            """
            SELECT title, imdb_rating, rotten_tomatoes, is_star_wars
            FROM MovieMetrics
            WHERE imdb_rating IS NOT NULL
            ORDER BY imdb_rating DESC
            LIMIT 10
        """
        )
        top_imdb = cursor.fetchall()

        # Top 10 by RT
        cursor.execute(
            """
            SELECT title, imdb_rating, rotten_tomatoes, is_star_wars
            FROM MovieMetrics
            WHERE rotten_tomatoes IS NOT NULL
            ORDER BY rotten_tomatoes DESC
            LIMIT 10
        """
        )
        top_rt = cursor.fetchall()

        return {
            "top_by_imdb": [
                {
                    "title": row[0],
                    "imdb": row[1] * 10,
                    "rt": row[2],
                    "is_star_wars": row[3],
                }
                for row in top_imdb
            ],
            "top_by_rt": [
                {
                    "title": row[0],
                    "imdb": row[1] * 10,
                    "rt": row[2],
                    "is_star_wars": row[3],
                }
                for row in top_rt
            ],
        }

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return {}

    finally:
        conn.close()


def write_omdb_calculations_to_file(filename="calculation_results.txt"):
    """
    Writes all OMDB calculations to a text file in clear, readable format.
    """
    try:
        with open(filename, "a") as f:
            f.write("\n\n")
            f.write("=" * 70 + "\n")
            f.write("STAR WARS vs ALL OTHER MOVIES - RATING ANALYSIS\n")
            f.write("=" * 70 + "\n\n")

            # CALCULATION 1: Average ratings comparison
            f.write("AVERAGE RATINGS COMPARISON\n")
            f.write("-" * 70 + "\n")

            averages = calculate_average_ratings_comparison()

            f.write(f"Star Wars Movies ({averages['star_wars']['count']} total):\n")
            f.write(
                f"  Average IMDb Rating:           {averages['star_wars']['imdb']:.1f}/100\n"
            )
            f.write(
                f"  Average Rotten Tomatoes Score: {averages['star_wars']['rt']:.1f}/100\n\n"
            )

            f.write(f"Other Movies ({averages['other_movies']['count']} total):\n")
            f.write(
                f"  Average IMDb Rating:           {averages['other_movies']['imdb']:.1f}/100\n"
            )
            f.write(
                f"  Average Rotten Tomatoes Score: {averages['other_movies']['rt']:.1f}/100\n\n"
            )

            # Calculate differences
            imdb_diff = averages["star_wars"]["imdb"] - averages["other_movies"]["imdb"]
            rt_diff = averages["star_wars"]["rt"] - averages["other_movies"]["rt"]

            f.write("Comparison:\n")
            f.write(f"  Star Wars IMDb is {abs(imdb_diff):.1f} points ")
            f.write("HIGHER\n" if imdb_diff > 0 else "LOWER\n")
            f.write(f"  Star Wars RT is {abs(rt_diff):.1f} points ")
            f.write("HIGHER\n" if rt_diff > 0 else "LOWER\n")

            # CALCULATION 2: Rating differences for Star Wars only
            f.write("\n\n")
            f.write("STAR WARS MOVIES - CRITIC vs AUDIENCE AGREEMENT\n")
            f.write("-" * 70 + "\n")
            f.write(f"{'Movie Title':<45} {'IMDb':<8} {'RT':<8} {'Diff':<8}\n")
            f.write("-" * 70 + "\n")

            all_diffs = calculate_rating_differences()
            sw_diffs = {k: v for k, v in all_diffs.items() if v["is_star_wars"]}

            for title, data in sorted(sw_diffs.items()):
                short_title = title[:42] + "..." if len(title) > 42 else title
                f.write(
                    f"{short_title:<45} "
                    f"{data['imdb']:>6.1f}  "
                    f"{data['rt']:>6.1f}  "
                    f"{data['difference']:>+6.1f}\n"
                )

            # CALCULATION 3: Top movies ranking
            f.write("\n\n")
            f.write("TOP 10 HIGHEST RATED MOVIES (ALL MOVIES)\n")
            f.write("-" * 70 + "\n")

            top_movies = calculate_top_rated_movies()

            f.write("By IMDb Rating:\n")
            for i, movie in enumerate(top_movies["top_by_imdb"], 1):
                marker = "[STAR WARS]" if movie["is_star_wars"] else "[Other]    "
                short_title = (
                    movie["title"][:40] + "..."
                    if len(movie["title"]) > 40
                    else movie["title"]
                )
                f.write(f"{i:2}. {marker} {short_title:<43} {movie['imdb']:.1f}\n")

            f.write("\nBy Rotten Tomatoes Score:\n")
            for i, movie in enumerate(top_movies["top_by_rt"], 1):
                marker = "[STAR WARS]" if movie["is_star_wars"] else "[Other]    "
                short_title = (
                    movie["title"][:40] + "..."
                    if len(movie["title"]) > 40
                    else movie["title"]
                )
                f.write(f"{i:2}. {marker} {short_title:<43} {movie['rt']:.0f}\n")

            f.write("\n" + "=" * 70 + "\n")

        print(f"Successfully wrote OMDB calculations to {filename}")

    except IOError as e:
        print(f"Error writing to file {filename}: {e}")


if __name__ == "__main__":
    # Comics calculations
    data = calculate_comics_per_year()
    print("Comics per year", data)
    write_comic_data(data)

    # OMDB calculations
    print("\nCalculating OMDB movie ratings comparisons...")

    averages = calculate_average_ratings_comparison()
    print(
        f"\nStar Wars average: IMDb {averages['star_wars']['imdb']:.1f}, RT {averages['star_wars']['rt']:.1f}"
    )
    print(
        f"Other movies average: IMDb {averages['other_movies']['imdb']:.1f}, RT {averages['other_movies']['rt']:.1f}"
    )

    diffs = calculate_rating_differences()
    print(f"\nTotal movies with ratings: {len(diffs)}")

    # Write OMDB calculations to file
    write_omdb_calculations_to_file()

    print("\nAll calculations complete!")

# LEGOLEGO LEGOOOO


def calculate_lego_complexity_by_year(db_filename="starwars.db"):
    """
    Calculates the average Lego set complexity (number of pieces)
    for each year in the lego_sets table.

    Returns:
        dict: {year: average_num_parts}
    """
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    query = """
    SELECT year, AVG(num_parts)
    FROM lego_sets
    WHERE year IS NOT NULL
      AND num_parts IS NOT NULL
    GROUP BY year
    ORDER BY year ASC;
    """

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        complexity_by_year = {year: avg_parts for year, avg_parts in results}
        return complexity_by_year

    except sqlite3.Error as e:
        print(f"Database error (Lego complexity by year): {e}")
        return {}

    finally:
        conn.close()


def calculate_top_lego_sets(limit=10, db_filename="starwars.db"):
    """
    Finds the most complex Lego sets by piece count.

    Returns:
        list[dict]: Each dict has keys: set_num, name, year, num_parts
    """
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    query = """
    SELECT s.set_num, n.name, s.year, s.num_parts
    FROM lego_sets s
    WHERE num_parts IS NOT NULL
    JOIN lego_set_names n ON s.name_id = n.id
    ORDER BY num_parts DESC
    LIMIT ?;
    """

    try:
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        top_sets = [
            {
                "set_num": row[0],
                "name": row[1],
                "year": row[2],
                "num_parts": row[3],
            }
            for row in rows
        ]
        return top_sets

    except sqlite3.Error as e:
        print(f"Database error (Top Lego sets): {e}")
        return []

    finally:
        conn.close()


def write_lego_calculations_to_file(filename="calculation_results.txt"):
    """
    Appends Lego-only complexity calculations to the text file.
    """
    try:
        with open(filename, "a") as f:
            f.write("\n\n")
            f.write("=" * 70 + "\n")
            f.write("LEGO SET COMPLEXITY ANALYSIS\n")
            f.write("=" * 70 + "\n\n")

            # CALCULATION 1: Average complexity by year
            f.write("AVERAGE LEGO COMPLEXITY BY YEAR\n")
            f.write("-" * 70 + "\n")

            complexity = calculate_lego_complexity_by_year()
            if not complexity:
                f.write("No Lego data available in the database.\n\n")
            else:
                for year, avg_parts in sorted(complexity.items()):
                    f.write(
                        f"Year: {year:<6} | "
                        f"Average Pieces per Set: {avg_parts:6.1f}\n"
                    )

            # CALCULATION 2: Top most complex Lego sets
            f.write("\nTOP MOST COMPLEX LEGO SETS (BY PART COUNT)\n")
            f.write("-" * 70 + "\n")

            top_sets = calculate_top_lego_sets()
            if not top_sets:
                f.write("No Lego sets found in the database.\n")
            else:
                for i, s in enumerate(top_sets, 1):
                    year_str = s["year"] if s["year"] is not None else "N/A"
                    f.write(
                        f"{i:2}. {s['name']} "
                        f"(Set {s['set_num']}, {year_str}) "
                        f"- {s['num_parts']} pieces\n"
                    )

            f.write("\n" + "=" * 70 + "\n")

            f.write("\nTOP 10 LEGO THEMES BY COMPLEXITY (AVG PARTS)\n")
            f.write("-" * 70 + "\n")

            # Call the new join function
            theme_stats = calculate_lego_theme_averages()

            if not theme_stats:
                f.write("No theme data available.\n")
            else:
                f.write(f"{'Theme Name':<40} {'Avg Parts':<10} {'Set Count':<10}\n")
                f.write("-" * 70 + "\n")
                for name, avg, count in theme_stats:
                    # Handle cases where name might be None
                    safe_name = name if name else "Unknown Theme"
                    f.write(f"{safe_name:<40} {avg:<10.1f} {count:<10}\n")

        print(f"Successfully wrote LEGO calculations to {filename}")

    except IOError as e:
        print(f"Error writing Lego calculations to file {filename}: {e}")


if __name__ == "__main__":
    # Quick manual test if you ever run this file directly
    print("\nWriting COMIC calculations...")
    print("Comics per year:", calculate_comics_per_year())
    write_comic_data(calculate_comics_per_year())

    print("\nWriting OMDB calculations...")
    write_omdb_calculations_to_file()

    print("\nWriting LEGO calculations...")
    write_lego_calculations_to_file()

    print("\nAll calculations complete!")
