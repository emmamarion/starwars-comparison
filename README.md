# 🚀 Final SI201 Project: starwars-comparison

## Team
**Names:** Emma Marion, Kamila Podsiadlo, Ava Anderson

---

## Instructions for Running Our Code

### 1. API Key Setup

This project requires API keys for two services: OMDb and Rebrickable.

| Service | Setup Link | Key Requirement |
| :--- | :--- | :--- |
| **OMDb** | [Sign up for OMDb API key here](https://www.omdbapi.com/apikey.aspx) | API Key |
| **Rebrickable** | [Create a Rebrickable account here](https://rebrickable.com/api/) | Generate an API Key from your profile's settings page. |

Once you have your keys, add them to the `api_keys.txt` file in the following format. **Ensure there is a space between the colon and the API key.**

### 2. Execution Steps

Follow these steps in order to run the project and generate the final results:

1.  **Run the database setup:**
    ```bash
    python database_setup.py
    ```

2.  **Run the data collection scripts:**
    * Run *each* script located in the `collection_files` folder at least **5 times** to satisfy the project requirements.
        ```bash
        python collection_files/collect_lego.py
        python collection_files/collect_omdb.py
        python collection_files/collect_wookiepedia.py
        # ... repeat 5 times for each
        ```

3.  **Run calculations:**
    ```bash
    python calculations.py
    ```

4.  **Run visualizations:**
    ```bash
    python visualizations.py
    ```

---

## Project Output

* The **database** file and **calculation results** files are saved directly into the root project folder.
* The **PNG visualization files** are saved to the `visualizations` folder.

---

## Important Notes and Limitations

### `collect_wookiepedia.py`
* While string data for comic names may look very similar to one another, they are unique. The reason for this is that Wookieepedia counts each edition of a comic as a separate entry. The database table creation uses the `UNIQUE` keyword for the comic name column to ensure only one entry per comic (edition) is stored.

### `collect_OMDB.py`
* **Limitation:** Movie names are **hardcoded**, which is a constraint imposed by the OMDb API.
* The `get_top_movies` function might return duplicate movies in its list. However, the `insert_into_database` function ensures that **duplicate movies are NOT added** to the database.
* The `insert_into_database` function performs 100 API calls every time the file is run, but it only inserts 25 new rows into the database, satisfying the project's data collection requirements.