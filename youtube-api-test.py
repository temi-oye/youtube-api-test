from dotenv import load_dotenv
import os
from googleapiclient.discovery import build

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

  res = get_videos_from_playlist(youtube, "PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS")
  print(res)
  
  youtube.close()

def get_videos_from_playlist(youtube, playlist_id):
  request = youtube.playlistItems().list(part="snippet", playlistId=playlist_id)
  response = request.execute()
  return response
  
if __name__ == "__main__":
  main()
