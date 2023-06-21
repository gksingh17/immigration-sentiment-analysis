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
import csv
from apiclient.errors import HttpError

def get_comments(youtube, vidId, commentInfo = [], pgtoken=""):
    request = youtube.commentThreads().list(
        part = "snippet,replies",
        videoId = vidId,
        pageToken = pgtoken,
        textFormat = "plainText"
        )
    response = request.execute()
    
    for item in response["items"]:
        parent_id = item["id"]
        topLevelComment = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
        authorName = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        likes = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
        datePublished = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]  
        topCommentInfo = (parent_id,authorName,likes,datePublished,topLevelComment)
        commentInfo.append(topCommentInfo)
        
        replies = youtube.comments().list(
            part="snippet",
            parentId = parent_id,
            textFormat="plainText"
            ).execute()
        
        for reply in replies["items"]:
            replyComment = reply["snippet"]["textOriginal"]
            commentId = reply["id"]
            authorName = reply["snippet"]["authorDisplayName"]
            likes = reply["snippet"]["likeCount"]
            datePublished = reply["snippet"]["publishedAt"]  
            replyCommentInfo = (commentId,authorName,likes,datePublished,replyComment)
            commentInfo.append(replyCommentInfo)

    if "nextPageToken" in response:
        return get_comments(youtube, vidId, commentInfo, response["nextPageToken"])
    else:
        return commentInfo         

if __name__ == "__main__":
    try:
        load_dotenv()
        api_key = os.getenv('CLIENT_SECRET')
        youtube = build('youtube', 'v3', developerKey=api_key)
        vidId = 'JLMeOkYUJ-Y'  # Would convert it as a command line argument for automation purpos.
        comments =  get_comments(youtube, vidId)
        with open('YoutubeComments.csv','w',encoding="utf-8") as csvFile:
            outFile = csv.writer(csvFile)
            outFile.writerow(['Id','AuthorName','LikeCount','Date Published','Comment Text'])
            for comment in comments:
                outFile.writerow(comment)
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
    else:
        print("Added Comments to csv")    