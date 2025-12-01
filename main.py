import database_setup
import calculations
import visualizations
from collection_files import collect_lego
from collection_files import collect_wookiepedia


def main():
    # SETUP DATABASE
    database_filename = "starwars.db"
    calc_results_filename = "calculation_results.txt"
    database_setup.database_setup(database_filename)

    # Webscrape wookiepedia
    html_content = collect_wookiepedia.collect_comics()
    total_rows_added = collect_wookiepedia.scrape(html_content, database_filename)
    print(f"Job complete. Total new comics added: {total_rows_added}")

    # Save wookiepedia results to txt
    comic_dict = calculations.calculate_comics_per_year(database_filename)
    calculations.write_comic_data(comic_dict, calc_results_filename)

    # Visualize wookiepedia comic data
    visualizations.plot_comics_by_year(comic_dict)

    # First api: SWAPI
    # swapi_data = collect_swapi.fetch_and_cache_data()

    # collect_swapi.seed_manufacturers(swapi_data, database_filename, limit=25)
    # collect_swapi.seed_vehicles(swapi_data, database_filename, limit=25)


if __name__ == "__main__":
    main()
