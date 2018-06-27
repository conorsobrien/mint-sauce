#!/usr/bin/python
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sqlite3


# Set DEVELOPER_KEY to the API key value from your own developer
key_file = open("google-api-key.txt")
DEVELOPER_KEY = key_file.readline().rstrip()
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Connect to sqllite database
conn = sqlite3.connect('fizzy-anvil')
cur = conn.cursor()

# Gather list of videos we've already found.
cur.execute('''SELECT id
                FROM videos
                where downloaded = 0
                and id = "BIkHTKk2xf0" ''')
all_rows = cur.fetchall()

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  developerKey=DEVELOPER_KEY)

# Replace the Q value with any query you'd like
search_response = youtube.search().list(
  q="Turin",
  channelId="UCNDJiDFJWaiKktyUBmVzGYA",
  type="video",
  part='id,snippet',
  maxResults=50
).execute()


# Set next page token for pagination
nextPageToken = search_response.get("nextPageToken",False)

results = search_response.get('items', [])
videos = []
titles = []
urls = []

for search_result in search_response.get('items', []):
  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  if search_result['id']['kind'] == 'youtube#video':
    videos.append('%s' % (search_result['snippet']['thumbnails']['high']['url']))
    titles.append('%s' % (search_result['snippet']['title']))
    urls.append('%s' % (search_result['id']))


# Iterate through pages of search results.
while nextPageToken:
  print("Before Next token: ",search_response['nextPageToken'])  
  search_response = youtube.search().list(
    q="Turin",
    channelId="UCNDJiDFJWaiKktyUBmVzGYA",
    type="video",
    part='id,snippet',
    pageToken = nextPageToken,
    maxResults=50
  ).execute()
  # Add results to results
  results.extend(search_response.get('items', []))
  # Reset next page token
  nextPageToken = search_response.get("nextPageToken",False)



# Iterate through results
for result in results:
#  print(result['id']['videoId'])
  video_response = youtube.videos().list(
    id=result['id']['videoId'],
    part='id,snippet,contentDetails'
  ).execute()
  duration = video_response['items'][0]['contentDetails']['duration']

  try:
    print(result['id']['videoId'] + " - " +  result['snippet']['title'] + " - " + duration)
    cur.execute('''INSERT INTO videos(id, title, processed, downloaded, length, split) VALUES(?, ? , ? , ?, ?, ?)''',(result['id']['videoId'], result['snippet']['title'], 1,0, duration,0))
    conn.commit()
    print("Processed")
  except Exception as e:
    print("Failed to write to DB. Error - " + e)
    print(e)

for title in titles:
	print(title)
conn.close()


