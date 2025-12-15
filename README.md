# Final SI201 project: starwars-comparison
<!-- TODO: ADD NAMES -->
**Names:** Emma Marion, Kamila Podsiadlo, Ava Anderson


Instructions for Running Our Code

Sign up for OMDB API key here: https://www.omdbapi.com/apikey.aspx

Create a Rebrickable account for an api key here: https://rebrickable.com/api/

Once an account is created,  generate an API Key from your profile's settings page.
Add API keys to the api_keys.txt file. Make sure to leave a space between the colon and the API key.

rebrickable: PUT_KEY_HERE
omdb: PUT_KEY_HERE

Run database_setup.py
Run each collect_().py file at least 5 times, located in the collection_files folder.
collect_lego.py
collect_omdb.py
collect_wookiepedia.py
Run calculations.py
Run visualizations.py
The database and calculation results files are saved directly into the root folder, while the PNG visualization files are saved to the visualizations folder, and PNG visualizations are saved directly into the project folder.
IMPORTANT NOTES:
collect_wookiepedia.py: 
While string data for comic names look very similar to one another, they are unique. The reason for them looking so similar is that wookiepedia counts each edition of a comic as a separate entry. When the table is created, the “unique” keyword is used for the name column.
collect_OMDB.py: 
Movie names are hardcoded, which is a limitation of OMDB. 
There might be duplicate movies in the “top movies” list from the get_top_movies function. However, duplicate movies are NOT added to the database.
Although the  insert_into_database does 100 API calls every time the file is run, it only inserts 25 new rows into the database. This satisfies the project requirements.