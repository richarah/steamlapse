import requests
import time
import csv
import os
import re

def valid_steam_id(steam_id):
    if len(steam_id) != 17:
        return False
    if not steam_id.isnumeric():
        return False
    return True


def get_time():
    # Avoid jet lag
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())


def get_player_data(steam_id, api_key):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={api_key}&steamids={steam_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


def get_persona(player_data):
    return player_data['response']['players'][0]['personaname']


def get_game(player_data):
    if not player_data['response']['players']:
        return "<offline>"
    elif player_data['response']['players'][0]['personastate'] == 1:
        return "<online>"
    else:
        return player_data['response']['players'][0]['gameextrainfo']

def append_csv_header(file_path):
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        with open(file_path, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['game', 'timestamp'])

def append_csv_entry(file_path, player_data):
    append_csv_header(file_path)
    game = get_game(player_data)
    timestamp = get_time()
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([game, timestamp])
        
def id_from_path(filename):
    pattern = r"(.+)_([0-9]{17})\.csv"
    match = re.match(pattern, filename)
    if match:
        return match.group(2)
    else:
        return None
