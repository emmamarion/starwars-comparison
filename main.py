import database_setup
import calculations
import visualizations
from collection_files import collect_lego
from collection_files import collect_swapi
from collection_files import collect_wookiepedia


def main():
    # SETUP DATABASE
    database_filename = "starwars.db"
    database_setup.database_setup(database_filename)

    # First api: SWAPI
    manufacturer_list = collect_swapi.get_manufacturer_data(database_filename)
    collect_swapi.update_manufacturer_table(
        manufacturer_list, database_filename, limit=25
    )


if __name__ == "__main__":
    main()
