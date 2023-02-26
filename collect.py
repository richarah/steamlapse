from modules import *
import os
import glob
from dotenv import load_dotenv

def main():
    while True:
        try:
            # Allow changing API key and files during runtime
            csv_files = glob.glob("./data/*.csv")
            load_dotenv()
            api_key = os.environ["STEAM_API_KEY"]
            for csv_file in csv_files:
                steam_id = id_from_path(csv_file)
                print("Querying Steam API with ID:", steam_id)
                if valid_steam_id(steam_id):
                    player_data = get_player_data(steam_id, api_key)
                    append_csv_entry(csv_file, player_data)
                    print("Entry appended to " + csv_file + ". Sleeping for 60 seconds.")
                    time.sleep(60)
                else:
                    print("ID", steam_id, "invalid")
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print("Retrying in 60 seconds.")
            time.sleep(0)
            
if __name__ == '__main__':
    main()
