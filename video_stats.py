import requests
import json
import os
from dotenv import load_dotenv

#read .env file
load_dotenv(dotenv_path='.env')
API_KEY = os.getenv('API_KEY')

CHANNEL_HANDLE = 'MrBeast'              #   or     CHANNEL_NAME = 'MrBeast'

def get_playlist_id():
    try : 
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

        reponse = requests.get(url)

        reponse.raise_for_status()

        data = reponse.json()

        json_object = json.dumps(data, indent=4)

        #print(json_object)

        channel_items = data['items'][0]
        channel_playlist_id = channel_items['contentDetails']['relatedPlaylists']['uploads']

        print(channel_playlist_id)
        #print(json_object) #optional

        return channel_playlist_id #show uploads playlist id
    
    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    get_playlist_id()