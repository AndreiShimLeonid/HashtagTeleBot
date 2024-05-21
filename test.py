import datetime
import sqlite3
timestamp = 1629398400
print(type(timestamp))
date_time = datetime.datetime.fromtimestamp(timestamp)
print(date_time.date())
print(date_time.strftime('%Y-%m-%d %H:%M:%S'))

conn = sqlite3.connect('hashtag_stats.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
SELECT * FROM hashtag_stats
''')

rows = cursor.fetchall()
for row in rows:
    print(f'user id: {row[0]}, username: {row[1]}, '
          f'date: {row[2]}, '
          f'hashtag: {row[3]}')

