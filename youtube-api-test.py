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
  request = youtube.channels().list(part="statistics", forUsername="GoogleDevelopers")
  response = request.execute()
  print(response)
  
  youtube.close()
  
if __name__ == "__main__":
  main()
