from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
import json
from datetime import datetime, timedelta
import re
from functools import reduce

def configure():
  load_dotenv()

def get_videos_ids_from_playlist(youtube, playlist_id):
  prev_request = youtube.playlistItems().list(part="snippet", playlistId=playlist_id, maxResults=50)
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

  return list(video_ids)

def get_duration_as_iso(youtube, video_id):
  request = youtube.videos().list(part="contentDetails", id=video_id)
  response = request.execute()
  iso = response["items"][0]["contentDetails"]["duration"]
  return iso

def get_duration_as_iso_all(youtube, videos_ids):
  video_iso_all = map(lambda id:get_duration_as_iso(youtube, id), videos_ids)
  return list(video_iso_all)

def iso_to_seconds(iso):
  hour_pattern = re.compile("\d+(?=H)")
  min_pattern = re.compile("\d+(?=M)")
  second_pattern = re.compile("\d+(?=S)")

  pattern_list = [hour_pattern, min_pattern, second_pattern]
  seconds = 0

  for current_pattern in pattern_list:
    match = current_pattern.search(iso)
    time = match.group(0) if match else 0
    time = int(time)

    if current_pattern == hour_pattern:
      seconds += time * 3600
    elif current_pattern == min_pattern:
      seconds += time * 60
    else:
      seconds += time

  return seconds

def get_playlist_watch_length_as_seconds(youtube, playlist_id):
  video_ids = get_videos_ids_from_playlist(youtube, playlist_id)
  iso_all = get_duration_as_iso_all(youtube, video_ids)
  seconds_all = list(map(lambda iso: iso_to_seconds(iso), iso_all))

  seconds_all_sum = reduce(lambda accumluator, seconds:accumluator+seconds, seconds_all)

  return seconds_all_sum

def main():
  configure()
  api_key = os.getenv("api_key")
  youtube = build('youtube', 'v3', developerKey=api_key)

  seconds = get_playlist_watch_length_as_seconds(youtube, "PLhQjrBD2T382_R182iC2gNZI9HzWFMC_8")
  m, s = divmod(seconds, 60)
  h, m = divmod(m, 60)

  print(f'It would take you: {h:d} hours, {m:02d}, minutes and {s:02d} seconds to watch this playlist')
 
  youtube.close()
  
if __name__ == "__main__":
  main()
