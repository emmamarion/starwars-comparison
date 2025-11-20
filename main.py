import database_setup
import calculations
import visualizations
from collection_files import collect_lego
from collection_files import collect_swapi
from collection_files import collect_wookiepedia


def main():
    database_filename = "starwars.db"

    database_setup.database_setup(database_filename)
    collect_swapi.update_character_table(
        collect_swapi.get_data("character", 1), database_filename
    )


if __name__ == "__main__":
    main()
