import os
import json
import time

from dotenv import load_dotenv
import requests

load_dotenv()  # take environment variables
user_id = os.environ['USER_ID']
api_token = os.environ['API_TOKEN']
headers = {
    'Authorization': f'Bearer {api_token}'
}

def get_user_info():
    response = requests.get(f'https://skylines.aero/api/users/{user_id}', headers=headers)
    response.raise_for_status()
    return response.json()


def get_flights():
    total_flights = None
    flights = []
    page = 1

    # last clause as precaution for inf loop
    while (total_flights is None or len(flights) < total_flights or page > 20):
        response = requests.get(f'https://skylines.aero/api/flights/pilot/{user_id}?page={page}', headers=headers)
        response.raise_for_status()

        flights.extend(response.json()['flights'])
        if total_flights is None:
            total_flights = response.json()['count']

        page += 1

    return flights


def download_igc(filename):
    response = requests.get(f'https://skylines.aero/files/{filename}', headers=headers)
    return response.text


def get_flight_info(flight_id):
    response = requests.get(f'https://skylines.aero/api/flights/{flight_id}/?extended', headers=headers)
    response.raise_for_status()
    return response.json()

#####################################

if not os.path.isdir('export'):
    os.mkdir('export')

if not os.path.isdir('export/igc_files'):
    os.mkdir('export/igc_files')

user_info = get_user_info()
with open('export/user_info.json', 'w') as f:
    json.dump(user_info, f)
    print('Exported userinfo: export_data/user_info.json')

flights = get_flights()
with open('export/flight_info.json', 'w') as f:
    json.dump(flights, f)
    print('Exported flights: export_data/flight_info.json')

for flight in flights:
    filename = flight['igcFile']['filename']

    igc_path = f'export/igc_files/{filename}'

    if os.path.exists(igc_path):
        print(f'{igc_path} already downloaded')
        continue

    igc_content = download_igc(filename)
    with open(igc_path,'w') as f:
        f.write(igc_content)
    print(f'{igc_path} downloaded')
    time.sleep(1) # do not hammer server

# get flight info
flight_info_extended = []
with open('export/flight_info.json') as f:
    flight_info = json.load(f)
for flight in flight_info:
    info = get_flight_info(flight['id'])
    print(f'succesfully gotten flight info for {flight["id"]}')
    flight_info_extended.append(info)
    time.sleep(1) # do not hammer server
with open('export/flight_info_extended.json', 'w') as f:
    json.dump(flight_info_extended, f)
