from googleapiclient.discovery import build
import os

api_key = os.environ.get('CLIENT_SECRET')
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