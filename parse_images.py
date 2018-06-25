from PIL import Image
import sqlite3

# Retrieve list of previously processed links from database. Don't want to re-process these if avoidable.
conn = sqlite3.connect('C:/sqllite/fizzy-anvil')
cur = conn.cursor()
cur.execute('''SELECT id
                FROM videos
                where downloaded = 1
                and split = 1
                and parsed = 0
                and id in ("BIkHTKk2xf0","A2KUqitayfw") ''')
all_rows = cur.fetchall()

i1 = Image.open('videos\\BIkHTKk2xf0\\frame27900.jpg')
i2 = Image.open('videos\\A2KUqitayfw\\frame14400.jpg')
assert i1.mode == i2.mode, "Different kinds of images."
assert i1.size == i2.size, "Different sizes."
 
pairs = zip(i1.getdata(), i2.getdata())
if len(i1.getbands()) == 1:
    # for gray-scale jpegs
    dif = sum(abs(p1-p2) for p1,p2 in pairs)
else:
    dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
 
ncomponents = i1.size[0] * i1.size[1] * 3
print ("Difference (percentage):", (dif / 255.0 * 100) / ncomponents)
