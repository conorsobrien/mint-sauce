import sqlite3
import os
from pytube import YouTube

print("Test")
# Open SQLLite connection
conn = sqlite3.connect('fizzy-anvil')
cur = conn.cursor()

# Retrieve list of previously processed links from database. Don't want to re-process these if avoidable.
cur.execute('''SELECT id
                FROM videos
                where downloaded = 0
		and length not like '%H%'
	''')
all_rows = cur.fetchall()
processed_videos = []
for row in all_rows:
    print(row[0])
    videoid = str(row[0])
    # Create directory to hold video
    if not os.path.exists("videos/" + videoid):
        os.makedirs("videos/" + videoid)

    # Download the video
    url = "https://www.youtube.com/watch?v=" + videoid
    yt = YouTube(url)
    print(yt.streams)
    print(yt.streams.filter(audio_codec=None, res="720p", fps=30).all())
    #stream = yt.streams.get_by_itag(136)
    stream = yt.streams.first()
    print(stream)
    stream.download('videos/' + videoid, filename=videoid)

    # Update status of the video.
    try:
        cur.execute('''UPDATE videos set downloaded = 1 where id = ?''',(videoid,))
        conn.commit()
        print("Processed")
    except Exception as e:
        print("Failed to write to DB")
        print(e)

conn.close()
