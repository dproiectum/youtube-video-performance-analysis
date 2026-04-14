import requests
import json
from datetime import date

# Load environment variables
import os
from dotenv import load_dotenv

#SET UP VARIABLES VALUES
##read .env file
load_dotenv(dotenv_path='.env')
API_KEY = os.getenv('API_KEY')

CHANNEL_HANDLE = 'MrBeast'              #   or     CHANNEL_NAME = 'MrBeast'

max_results = 50

##############################################################################################################################################################################  

#I will modify to stock this function in a module to be imported in other scripts
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



def get_videos_ids(playlistId):
    video_ids = []

    pageToken = None
    
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlistId}&key={API_KEY}"

    try:
        
        while True:
            url = base_url

            if pageToken:
                url += f"&pageToken={pageToken}"
            
            response = requests.get(url)

            response.raise_for_status()
            
            data = response.json()
            
            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)
            
            pageToken = data.get('nextPageToken')

            if not pageToken:
                break

        return video_ids
    
    except requests.exceptions.RequestException as e:
        raise e 

def extract_video_data(video_ids):

    extracted_data = []

    def batch_list(video_id_list, batch_size):
        for video_id in range(0, len(video_id_list), batch_size):
            yield video_id_list[video_id : video_id + batch_size]

    try:
        for batch in batch_list(video_ids, max_results):
            video_ids_string = ','.join(batch)

            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_string}&key={API_KEY}"

            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            for item in data.get('items', []):
                video_info = {
                    'video_id': item['id'],
                    'title': item['snippet']['title'],
                    'publishedAt': item['snippet']['publishedAt'],
                    'duration': item['contentDetails']['duration'],

                    'viewCount': item['statistics'].get('viewCount', None),
                    'likeCount': item['statistics'].get('likeCount', None),
                    'commentCount': item['statistics'].get('commentCount', None)
                }
            
                extracted_data.append(video_info)
            
        return extracted_data 

    except requests.exceptions.RequestException as e:
        raise e

def save_to_json(extracted_data):
    file_path = f'./data/youtube_data_{date.today()}.json'


    with open(file_path, 'w', encoding='utf-8') as json_outfile:
        json.dump(extracted_data, json_outfile, indent=4, ensure_ascii=False)        


if __name__ == "__main__":
    playlistId = get_playlist_id()
    video_ids = get_videos_ids(playlistId)
    video_data = extract_video_data(video_ids)
    save_to_json(video_data)
    print("Data saved to JSON file.")   