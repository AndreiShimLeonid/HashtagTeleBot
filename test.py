import datetime

timestamp = 1629398400
date_time = datetime.datetime.fromtimestamp(timestamp)
print(date_time.date())
print(date_time.strftime('%Y-%m-%d %H:%M:%S'))