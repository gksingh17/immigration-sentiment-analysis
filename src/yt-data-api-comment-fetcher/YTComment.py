# (For Windows) 
# pip install virtualenv
# virtualenv yt-comment-fetcher
# yt-comment-fetcher\Scripts\activate
# yt-comment-fetcher\Scripts\pip.exe install google-api-python-client

# (For Mac/Linux) 
# pip3 install virtualenv
# virtualenv yt-comment-fetcher
# source yt-comment-fetcher/bin/activate
# yt-comment-fetcher/bin/pip install google-api-python-client

from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('CLIENT_SECRET')
youtube = build('youtube', 'v3', developerKey=api_key)
vidId = '-bpkiObJMCY'
request = youtube.commentThreads().list(
    part = "snippet",
    videoId = vidId,
    textFormat = "plainText"
)

response = request.execute()
print(response)