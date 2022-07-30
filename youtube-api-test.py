from dotenv import load_dotenv
import os


def configure():
  load_dotenv()

def main():
  configure()

main()

print(os.getenv("api_key"))