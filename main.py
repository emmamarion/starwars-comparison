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

# Please let me know if I am supposed to add this here, i feel like it makes sense
    print("\nCollecting Lego set data from Rebrickable...")
    lego_added = collect_lego.insert_lego_sets(limit=25)
    print(f"Total new Lego sets added this run: {lego_added}")

    # Lego-only calculations written to file
    calculations.write_lego_calculations_to_file(calc_results_filename)

    # Lego vs Star Wars movie comparison written to file
    calculations.write_lego_vs_star_wars_to_file(calc_results_filename)

    # Lego visualizations will be added in visualizations.py
    # e.g.:
    # visualizations.plot_lego_complexity_by_year()
    # visualizations.plot_lego_vs_star_wars_overall()







if __name__ == "__main__":
    main()
