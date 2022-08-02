from stringprep import map_table_b2
from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
import json

def configure():
  load_dotenv()

def main():
  configure()
  api_key = os.getenv("api_key")
  youtube = build('youtube', 'v3', developerKey=api_key)

  # there is no consistent method of getting the id or username of a channel as far as I know
  # request = youtube.channels().list(part="statistics", forUsername="INSIDERfood")
  # response = request.execute()
  # print(response)


  video_ids = get_videos_ids_from_playlist(youtube, "PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS")

  print(get_duration_as_iso_all(youtube, video_ids))

  youtube.close()

def get_videos_ids_from_playlist(youtube, playlist_id):
  prev_request = youtube.playlistItems().list(part="snippet", playlistId=playlist_id, maxResults=5)
  prev_response = prev_request.execute()
  is_next_page = "nextPageToken" in prev_response
  videos = prev_response["items"]  
  # print(json.dumps(videos, indent=4))

  while is_next_page:
    new_request = youtube.playlistItems().list_next(previous_request=prev_request, previous_response=prev_response)
    new_response = new_request.execute()
    is_next_page = "nextPageToken" in new_response
    videos += new_response["items"]
    
    prev_request = new_request
    prev_response = new_response

  video_ids = map(lambda video: video["snippet"]["resourceId"]["videoId"], videos)
  # video_ids = map(lambda video:get_duration_as_iso(youtube, video["snippet"]["resourceId"]["videoId"]), videos)
  # replaces all video ids with their duration (iso) 
  return list(video_ids)

def get_duration_as_iso_all(youtube, videos_ids):
  video_iso_all = map(lambda id:get_duration_as_iso(youtube, id), videos_ids)
  return list(video_iso_all)

def get_duration_as_iso(youtube, video_id):
  request = youtube.videos().list(part="contentDetails", id=video_id)
  response = request.execute()
  iso = response["items"][0]["contentDetails"]["duration"]
  return iso

  
if __name__ == "__main__":
  main()
