import database_setup
import calculations
import visualizations
from collection_files import collect_lego
from collection_files import collect_wookiepedia


def main():
    # SETUP DATABASE
    database_filename = "starwars.db"
    database_setup.database_setup(database_filename)

    # First api: SWAPI
    # swapi_data = collect_swapi.fetch_and_cache_data()

    # collect_swapi.seed_manufacturers(swapi_data, database_filename, limit=25)
    # collect_swapi.seed_vehicles(swapi_data, database_filename, limit=25)


if __name__ == "__main__":
    main()
