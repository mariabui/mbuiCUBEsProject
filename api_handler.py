import sys
import requests
from secrets import wufoo_key
from requests.auth import HTTPBasicAuth


def get_response(url: str) -> requests.Response:
    response = requests.get(url, auth=HTTPBasicAuth(wufoo_key, 'pass'))
    if response.status_code != 200:
        print(f'Failed to get data, response code: {response.status_code} and error message: {response.reason}')
        sys.exit(-1)
    return response


def convert_response_to_json(response: requests.Response) -> dict:
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError as json_decode_error:
        print(f'Failed to get data, JSON decode error: {json_decode_error}')
        sys.exit(-1)


def get_entries(url: str) -> list[dict]:
    url = f'{url}?pageStart=0&pageSize=100'
    response = get_response(url)
    json_response = convert_response_to_json(response)
    return json_response['Entries']


def save_entries_to_text_file(entries: list[dict], txt_filename: str):
    with open(txt_filename, 'w') as text_file:
        for entry in entries:
            for key, value in entry.items():
                print(f'{key}: {value}', file=text_file)
            print(file=text_file)
