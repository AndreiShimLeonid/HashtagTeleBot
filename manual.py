import db
# # {"id": 336055079, "first_name": "Сергей", "last_name": "Никольский", "username": "Sergey_aka_Nikola", "language_code": null, "is_bot": false}
# # def update_stats(user_id, username, name, date, hashtag):
# # {"id": 911448456, "first_name": "Эми", "last_name": "Грек", "username": "e_mi_grek", "language_code": null, "is_bot": false}
#
# db.update_stats(911448456, 'e_mi_grek', 'Эми Грек', date='2024-05-24', hashtag='#недобрый')
# db.update_stats(336055079, 'Sergey_aka_Nikola', 'Сергей Никольский', date='2024-05-01', hashtag='#добрый')
# db.update_stats(336055079, 'Sergey_aka_Nikola', 'Сергей Никольский', date='2024-05-02', hashtag='#добрый')
# db.update_stats(336055079, 'Sergey_aka_Nikola', 'Сергей Никольский', date='2024-05-03', hashtag='#добрый')
# db.update_stats(336055079, 'Sergey_aka_Nikola', 'Сергей Никольский', date='2024-05-09', hashtag='#добрый')
# db.update_stats(336055079, 'Sergey_aka_Nikola', 'Сергей Никольский', date='2024-05-11', hashtag='#добрый')
# db.update_stats(336055079, 'Sergey_aka_Nikola', 'Сергей Никольский', date='2024-05-14', hashtag='#добрый')
# db.update_stats(336055079, 'Sergey_aka_Nikola', 'Сергей Никольский', date='2024-05-15', hashtag='#добрый')
# db.update_stats(336055079, 'Sergey_aka_Nikola', 'Сергей Никольский', date='2024-05-16', hashtag='#добрый')
# db.update_stats(336055079, 'Sergey_aka_Nikola', 'Сергей Никольский', date='2024-05-17', hashtag='#добрый')
# db.update_stats(336055079, 'Sergey_aka_Nikola', 'Сергей Никольский', date='2024-05-18', hashtag='#добрый')
# db.update_stats(336055079, 'Sergey_aka_Nikola', 'Сергей Никольский', date='2024-05-20', hashtag='#добрый')
# db.update_stats(336055079, 'Sergey_aka_Nikola', 'Сергей Никольский', date='2024-05-21', hashtag='#добрый')
# db.update_stats(336055079, 'Sergey_aka_Nikola', 'Сергей Никольский', date='2024-05-22', hashtag='#добрый')
# with open('report.txt', 'r') as file:
#     rows = file.readlines()
#     data = []
#     for row in rows:
#         splitted_row = row.replace('\n', '').split(",")
#         new_row = []
#         for item in splitted_row:
#             new_row.append(item.strip())
#         data.append(new_row)
#     print(data)
# for item in data:
#     db.update_stats(user_id=item[1], username=item[3], name=item[2], date=item[4], hashtag=item[5])
db.update_stats(336055079, 'Sergey_aka_Nikola', 'Сергей Никольский', date='2024-05-23', hashtag='#добрый')
db.update_stats(418857789, None, 'ssk', date='2024-05-25', hashtag='#добрый')
# import sqlite3
#
# import db
#
# # Подключение к базе данных
# conn = sqlite3.connect(db.stats_db_name)
# cursor = conn.cursor()
#
# # Создание таблицы, если она не существует
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS hashtag_stats (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         user_id INTEGER,
#         name TEXT,
#         username TEXT,
#         date TEXT,
#         hashtag TEXT,
#         UNIQUE(user_id, username, date, hashtag)
#     )
# ''')
#
# # Обновление значений 'Unknown' на NULL в столбце username
# cursor.execute('''
#     UPDATE hashtag_stats
#     SET username = NULL
#     WHERE username = 'Unknown'
# ''')
#
# # Сохранение изменений
# conn.commit()
#
# # Закрытие соединения
# conn.close()