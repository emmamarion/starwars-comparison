import matplotlib.pyplot as plt
import sqlite3


def plot_comics_by_year(data):
    """
    Creates a bar chart showing the number of comics released per year.

    Args:
        data (dict): A dictionary where keys are years (str or int) and values are counts (int).
    """
    if not data:
        print("No data to visualize.")
        return

    try:
        sorted_years = sorted(data.keys(), key=lambda x: int(x))
    except ValueError:
        print("WARNING: dict keys are not convertable to ints")
        sorted_years = sorted(data.keys())

    counts = [data[year] for year in sorted_years]

    plt.figure(figsize=(12, 6))
    plt.bar(sorted_years, counts, color="#3b8ed0", edgecolor="black", zorder=3)

    # Titles and labels
    plt.title(
        "Star Wars Comics Released Per Year (Canon)", fontsize=16, fontweight="bold"
    )
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Number of releases", fontsize=12)

    # Rotate x-axis labels 45 degrees to prevent overlapping text
    plt.xticks(rotation=45, ha="right")

    # Add a subtle grid behind the bars for better readability
    plt.grid(axis="y", linestyle="--", alpha=0.7, zorder=0)

    # Automatically adjust subplot parameters to give specified padding
    plt.tight_layout()

    # Save image
    plt.savefig("visualizations/lego_comics.png", dpi=300, bbox_inches="tight")
    print("[OK] Saved: lego_vs_star_wars_overall.png")

    # Display the plot
    plt.show()


# ============================================================================
# OMDB VISUALIZATIONS - Kamila Podsiadlo (kampod@umich.edu)
# Clean visualizations comparing Star Wars to all collected movies
# ============================================================================


def plot_star_wars_rating_differences(db_filename="starwars.db"):
    """
    REQUIRED VISUALIZATION: Bar chart showing IMDb vs RT differences for Star Wars.
    Shows which Star Wars movies have agreement/disagreement between critics and audiences.
    """
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT title, imdb_rating, rotten_tomatoes
        FROM MovieMetrics
        WHERE imdb_rating IS NOT NULL 
        AND rotten_tomatoes IS NOT NULL
        AND is_star_wars = 1
        ORDER BY (imdb_rating * 10 - rotten_tomatoes) DESC
    """
    )

    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No Star Wars movie data to visualize.")
        return

    movies = []
    differences = []

    for title, imdb_rating, rt_score in rows:
        # Shorten titles
        short_title = title.replace("Star Wars: Episode ", "EP ")
        short_title = short_title.replace(" - A Star Wars Story", "")
        short_title = short_title.replace("Star Wars: ", "")
        movies.append(short_title)
        differences.append(imdb_rating * 10 - rt_score)

    # Create plot
    fig, ax = plt.subplots(figsize=(14, 8))

    colors = ["#3498db" if diff > 0 else "#e74c3c" for diff in differences]
    bars = ax.bar(
        range(len(movies)),
        differences,
        color=colors,
        edgecolor="black",
        linewidth=1.5,
        alpha=0.85,
    )

    # Zero line
    ax.axhline(y=0, color="black", linestyle="-", linewidth=2)

    # Labels and title
    ax.set_xlabel("Star Wars Movies", fontsize=13, fontweight="bold")
    ax.set_ylabel(
        "Rating Difference (IMDb - Rotten Tomatoes)", fontsize=13, fontweight="bold"
    )
    ax.set_title(
        "Star Wars: Do Audiences and Critics Agree?\n"
        + "Positive = Audiences rated higher (IMDb) | Negative = Critics rated higher (RT)",
        fontsize=15,
        fontweight="bold",
        pad=20,
    )

    ax.set_xticks(range(len(movies)))
    ax.set_xticklabels(movies, rotation=45, ha="right", fontsize=10)

    # Add value labels
    for bar, diff in zip(bars, differences):
        height = bar.get_height()
        label_y = height + (0.5 if height > 0 else -0.5)
        va = "bottom" if height > 0 else "top"
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            label_y,
            f"{diff:+.1f}",
            ha="center",
            va=va,
            fontsize=9,
            fontweight="bold",
        )

    ax.grid(axis="y", linestyle="--", alpha=0.4)

    # Legend
    from matplotlib.patches import Patch

    legend_elements = [
        Patch(facecolor="#3498db", edgecolor="black", label="Audiences liked more"),
        Patch(facecolor="#e74c3c", edgecolor="black", label="Critics liked more"),
    ]
    ax.legend(handles=legend_elements, loc="upper right", fontsize=11)

    plt.tight_layout()
    plt.savefig(
        "visualizations/star_wars_rating_differences.png", dpi=300, bbox_inches="tight"
    )
    print("[OK] Saved: star_wars_rating_differences.png")
    plt.show()


def plot_star_wars_vs_all_averages(db_filename="starwars.db"):
    """
    EXTRA VISUALIZATION #1: Compare Star Wars average ratings to all other movies.
    Shows if Star Wars rates higher or lower than the other collected films.
    """
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()

    # Star Wars averages
    cur.execute(
        """
        SELECT AVG(imdb_rating), AVG(rotten_tomatoes), COUNT(*)
        FROM MovieMetrics
        WHERE is_star_wars = 1 
        AND imdb_rating IS NOT NULL 
        AND rotten_tomatoes IS NOT NULL
    """
    )
    sw_result = cur.fetchone()
    sw_imdb = sw_result[0] * 10 if sw_result[0] else 0
    sw_rt = sw_result[1] if sw_result[1] else 0
    sw_count = sw_result[2]

    # Other movies averages
    cur.execute(
        """
        SELECT AVG(imdb_rating), AVG(rotten_tomatoes), COUNT(*)
        FROM MovieMetrics
        WHERE is_star_wars = 0 
        AND imdb_rating IS NOT NULL 
        AND rotten_tomatoes IS NOT NULL
    """
    )
    other_result = cur.fetchone()
    other_imdb = other_result[0] * 10 if other_result[0] else 0
    other_rt = other_result[1] if other_result[1] else 0
    other_count = other_result[2]

    conn.close()

    # Create side-by-side comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    categories = [
        f"Star Wars\n({sw_count} movies)",
        f"Top Movies\n({other_count} movies)",
    ]

    # IMDb comparison
    imdb_scores = [sw_imdb, other_imdb]
    colors_imdb = ["#FFD700", "#95a5a6"]  # Gold for Star Wars, gray for others

    bars1 = ax1.bar(
        categories,
        imdb_scores,
        color=colors_imdb,
        edgecolor="black",
        linewidth=2,
        width=0.6,
        alpha=0.9,
    )
    ax1.set_ylabel("Average IMDb Rating (0-100)", fontsize=12, fontweight="bold")
    ax1.set_title("IMDb Ratings\n(Audience Scores)", fontsize=14, fontweight="bold")
    ax1.set_ylim(0, 100)
    ax1.grid(axis="y", linestyle="--", alpha=0.3)

    for bar, score in zip(bars1, imdb_scores):
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 2,
            f"{score:.1f}",
            ha="center",
            va="bottom",
            fontsize=14,
            fontweight="bold",
        )

    # RT comparison
    rt_scores = [sw_rt, other_rt]
    colors_rt = ["#FFD700", "#95a5a6"]

    bars2 = ax2.bar(
        categories,
        rt_scores,
        color=colors_rt,
        edgecolor="black",
        linewidth=2,
        width=0.6,
        alpha=0.9,
    )
    ax2.set_ylabel(
        "Average Rotten Tomatoes Score (0-100)", fontsize=12, fontweight="bold"
    )
    ax2.set_title(
        "Rotten Tomatoes Scores\n(Critic Scores)", fontsize=14, fontweight="bold"
    )
    ax2.set_ylim(0, 100)
    ax2.grid(axis="y", linestyle="--", alpha=0.3)

    for bar, score in zip(bars2, rt_scores):
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 2,
            f"{score:.1f}",
            ha="center",
            va="bottom",
            fontsize=14,
            fontweight="bold",
        )

    plt.suptitle(
        "Star Wars vs Top Movies: Average Ratings Comparison",
        fontsize=16,
        fontweight="bold",
        y=0.98,
    )

    plt.tight_layout()
    plt.savefig(
        "visualizations/star_wars_vs_all_averages.png", dpi=300, bbox_inches="tight"
    )
    print("[OK] Saved: star_wars_vs_all_averages.png")
    plt.show()


def plot_top_movies_with_star_wars_highlighted(db_filename="starwars.db"):
    """
    EXTRA VISUALIZATION #2: Top 15 movies with Star Wars highlighted.
    Shows where Star Wars movies rank among all collected films.
    """
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT title, imdb_rating, rotten_tomatoes, is_star_wars
        FROM MovieMetrics
        WHERE imdb_rating IS NOT NULL AND rotten_tomatoes IS NOT NULL
        ORDER BY (imdb_rating * 10 + rotten_tomatoes) / 2 DESC
        LIMIT 15
    """
    )

    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No data for ranking visualization.")
        return

    titles = []
    avg_ratings = []
    colors = []

    for title, imdb, rt, is_sw in rows:
        # Shorten titles
        short_title = title[:45] + "..." if len(title) > 45 else title
        titles.append(short_title)
        avg_ratings.append((imdb * 10 + rt) / 2)
        colors.append("#FFD700" if is_sw else "#3498db")  # Gold for Star Wars

    # Create plot
    fig, ax = plt.subplots(figsize=(12, 10))

    bars = ax.barh(
        range(len(titles)),
        avg_ratings,
        color=colors,
        edgecolor="black",
        linewidth=1.5,
        alpha=0.85,
    )

    ax.set_xlabel("Average Rating (IMDb + RT) / 2", fontsize=12, fontweight="bold")
    ax.set_title(
        "How Do the Best Star Wars Movies Rank in the Top 15 Movies?\nGold = Star Wars | Blue = Top Movies",
        fontsize=14,
        fontweight="bold",
        pad=20,
    )

    ax.set_yticks(range(len(titles)))
    ax.set_yticklabels(titles, fontsize=10)
    ax.invert_yaxis()  # Highest at top
    ax.set_xlim(0, 100)

    # Add value labels
    for bar, rating in zip(bars, avg_ratings):
        width = bar.get_width()
        ax.text(
            width + 1,
            bar.get_y() + bar.get_height() / 2.0,
            f"{rating:.1f}",
            ha="left",
            va="center",
            fontsize=9,
            fontweight="bold",
        )

    ax.grid(axis="x", linestyle="--", alpha=0.3)

    # Legend
    from matplotlib.patches import Patch

    legend_elements = [
        Patch(facecolor="#FFD700", edgecolor="black", label="Star Wars Movies"),
        Patch(facecolor="#3498db", edgecolor="black", label="Top Movies"),
    ]
    ax.legend(handles=legend_elements, loc="lower center", fontsize=11)

    plt.tight_layout()
    plt.savefig("visualizations/top_movies_ranking.png", dpi=300, bbox_inches="tight")
    print("[OK] Saved: top_movies_ranking.png")
    plt.show()


# LEGOOOO TIMEEEEE
def plot_lego_complexity_by_year(db_filename="starwars.db"):
    """
    Creates a bar chart showing the average number of pieces
    per Lego set for each release year.

    Data source: lego_sets table (from Rebrickable API).
    """
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()

    # Get average num_parts per year, ignoring NULLs
    cur.execute(
        """
        SELECT year, AVG(num_parts), COUNT(*)
        FROM lego_sets
        WHERE year IS NOT NULL
          AND num_parts IS NOT NULL
        GROUP BY year
        ORDER BY year ASC
    """
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No Lego data available for visualization.")
        return

    years = [row[0] for row in rows]
    avg_parts = [row[1] for row in rows]
    counts = [row[2] for row in rows]  # in case you want to mention it in your report

    # Convert years to strings for nicer x-axis labels
    years_str = [str(y) for y in years]

    plt.figure(figsize=(12, 6))
    plt.bar(years_str, avg_parts, color="#2ecc71", edgecolor="black", zorder=3)

    # Titles and labels
    plt.title(
        "Average LEGO Set Complexity by Release Year", fontsize=16, fontweight="bold"
    )
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Average Number of Pieces per Set", fontsize=12)

    # Rotate x-axis labels so they don't overlap
    plt.xticks(rotation=45, ha="right")

    # Add subtle grid behind bars
    plt.grid(axis="y", linestyle="--", alpha=0.7, zorder=0)

    plt.tight_layout()
    plt.savefig(
        "visualizations/lego_complexity_by_year.png", dpi=300, bbox_inches="tight"
    )
    print("[OK] Saved: lego_complexity_by_year.png")

    plt.show()


if __name__ == "__main__":
    print("Creating visualizations...")

    # Comics visualization
    from calculations import calculate_comics_per_year

    data = calculate_comics_per_year()
    plot_comics_by_year(data)

    # OMDB visualizations
    print("\n1. Required: Star Wars rating differences...")
    plot_star_wars_rating_differences()

    print("\n2. Extra #1: Star Wars vs All Movies averages...")
    plot_star_wars_vs_all_averages()

    print("\n3. Extra #2: Top movies with Star Wars highlighted...")
    plot_top_movies_with_star_wars_highlighted()

    # Rebrickable visualizations
    plot_lego_complexity_by_year()
    plot_lego_vs_star_wars_overall()
    print("\nAll visualizations complete!")
