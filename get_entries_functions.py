import sys
import requests
from secrets import wufoo_key
from requests.auth import HTTPBasicAuth


def get_response(url):
    response = requests.get(url, auth=HTTPBasicAuth(wufoo_key, 'pass'))
    if response.status_code != 200:
        print(f'Failed to get data, response code: {response.status_code} and error message: {response.reason}')
        sys.exit(-1)
    return response


def convert_response_to_json(response):
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError as json_decode_error:
        print(f'Failed to get data, JSON decode error: {json_decode_error}')
        sys.exit(-1)


def get_entries(url) -> list[dict]:
    url = f'{url}?pageStart=0&pageSize=100'
    response = get_response(url)
    json_response = convert_response_to_json(response)
    return json_response['Entries']


def save_entries_to_text_file(entries, filename):
    with open(filename, 'w') as text_file:
        for entry in entries:
            print(entry, end='\n\n', file=text_file)
