import sqlite3
import os
import cv2
from pytube import YouTube

# Open SQLLite connection
conn = sqlite3.connect('fizzy-anvil')
cur = conn.cursor()

# Retrieve list of previously processed links from database. Don't want to re-process these if avoidable.
cur.execute('''SELECT id
                FROM videos
                where downloaded = 1
                and (split is null or split = 0)
            ''')
all_rows = cur.fetchall()

# Iterate through results 
for row in all_rows:
    print("Processing video: " + row[0])

    # Source: https://stackoverflow.com/questions/22704936/reading-every-nth-frame-from-videocapture-in-opencv
    videoid = str(row[0])
    vidcap = cv2.VideoCapture("videos" + videoid + "/" + videoid + '.mp4')
    #vidcap = cv2.VideoCapture("C:\\Users\\briecono\\Documents\\Personal\\Data Science\\Projects\\Fizzy Anvil\\videos\\BIkHTKk2xf0\\BIkHTKk2xf0.mp4")
    print(vidcap)
    success,image = vidcap.read()

    seconds = 30
    fps = vidcap.get(cv2.CAP_PROP_FPS) # Gets the frames per second
    multiplier = fps * seconds

    while success:
        frameId = int(round(vidcap.get(1))) #current frame number, rounded b/c sometimes you get frame intervals which aren't integers...this adds a little imprecision but is likely good enough
        success, image = vidcap.read()

        if frameId % multiplier == 0:
            cv2.imwrite("videos/" + videoid + "/frame%d.jpg" % frameId, image)

    vidcap.release()
    print("Complete")

     # Update status of the video.
    try:
        cur.execute('''UPDATE videos set split = 1 where id = ?''',(videoid,))
        conn.commit()
        print("DB split written")
    except Exception as e:
        print("Failed to write to DB")
        print(e)

conn.close()
