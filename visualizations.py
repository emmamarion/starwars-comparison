import matplotlib.pyplot as plt


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

    # Display the plot
    plt.show()
