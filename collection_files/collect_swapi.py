import requests
import os


def get_character(character_id=1):
    """
    creates an API request to the swapi
    ARGUMENTS:
        character_id: the id of the character
    """

    base_url = "http://swapi.dev/api/people/"

    # convert the character id to a string to append to url
    character_id_str = str(character_id)

    request_url = base_url + character_id_str
    response = requests.get(request_url)

    if response.status_code == 200:  # if the response was successful
        character_data = response.json()
        # TODO: finish function

    pass


# For debugging
def test():
    get_character()


test()
