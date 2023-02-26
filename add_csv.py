from modules import *
import os
from dotenv import load_dotenv

def create_csv_file(steam_id):
    load_dotenv()
    api_key = os.environ["STEAM_API_KEY"]
    player_data = get_player_data(steam_id, api_key)
    persona = get_persona(player_data)
    game = get_game(player_data)
    timestamp = get_time()
    filename = f'{persona}_{steam_id}.csv'
    filepath = os.path.join('data', filename)
    append_csv_entry(filepath, player_data)
    print("Saved to", filepath)

def main():
    steam_id = input("Steam ID (17 digits): ")
    create_csv_file(steam_id)
    
if __name__ == '__main__':
    main()
