from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
# api_key = os.environ.get('CLIENT_SECRET')
load_dotenv()

api_key = os.getenv('CLIENT_SECRET')
print(api_key)

youtube = build('youtube', 'v3', developerKey=api_key)
vidId = '-bpkiObJMCY'
request = youtube.commentThreads().list(
    part = "snippet",
    videoId = vidId,
    textFormat = "plainText"
)

response = request.execute()
youtube.close()
print(response)