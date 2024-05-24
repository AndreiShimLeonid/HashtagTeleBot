import datetime
import unittest
import sqlite3
import random
from datetime import datetime, timedelta

import db
from db import update_stats, get_stats, get_top_users, get_monthly_report, get_yearly_report
timestamp = 1629398400
print(type(timestamp))
date_time = datetime.fromtimestamp(timestamp)
print(date_time.date())
print(date_time.strftime('%Y-%m-%d %H:%M:%S'))

# conn = sqlite3.connect('hashtag_stats.db', check_same_thread=False)
# cursor = conn.cursor()
# cursor.execute('''
# SELECT * FROM hashtag_stats
# ''')
#
# rows = cursor.fetchall()
# for row in rows:
#     print(f'user id: {row[0]}, username: {row[1]}, '
#           f'date: {row[2]}, '
#           f'hashtag: {row[3]}')
#
# cursor.close()
# conn.close()
# days = [i for i in range(10, 28)]
# months = [i for i in range(1, 10)]
# users = [['user1', 1], ['user2', 2], ['user3', 3], ['user4', 4], ['user5', 5], ['user6', 6], ['user7',  7]]
# hashtags = ['#добрый', '#недобрый']
# for i in range(1000):
#     user, user_id = random.choice(users)
#     date = f'2024-0{random.choice(months)}-{random.choice(days)}'
#     hashtag = random.choice(hashtags)
#     update_stats(user_id, user, date, hashtag)

db.add_user(user_id=1, first_name='Andrei', last_name='Shim', username='aka_Andrei')
db.remove_user(user_id=1, username='aka_Andrei')

update_stats(1357737507, 'shimandrei', '2024-04-01', '#добрый')
update_stats(1357737507, 'shimandrei', '2024-04-02', '#добрый')
update_stats(1357737507, 'shimandrei', '2024-04-03', '#добрый')
update_stats(1357737507, 'shimandrei', '2024-04-04', '#добрый')
update_stats(1357737507, 'shimandrei', '2024-04-05', '#добрый')
update_stats(1357737507, 'shimandrei', '2024-04-05', '#недобрый')
# update_stats(1, 'user2', self.previous_date, '#hashtag1')
# update_stats(1, 'user3', self.previous_date, '#hashtag1')
# update_stats(1, 'user4', self.previous_date, '#hashtag1')
# update_stats(1, 'user1', self.previous_date, '#hashtag1')
# update_stats(1, 'user1', self.previous_date, '#hashtag1')
# update_stats(1, 'user1', self.previous_date, '#hashtag1')
# update_stats(1, 'user1', self.previous_date, '#hashtag1')


# class TestBotFunctions(unittest.TestCase):
#     def setUp(self):
#         # Создаем тестовую базу данных в памяти
#         self.conn = sqlite3.connect(':memory:')
#         self.cursor = self.conn.cursor()
#         self.cursor.execute('''
#         CREATE TABLE hashtag_stats (
#             user_id INTEGER,
#             username TEXT,
#             date TEXT,
#             hashtag TEXT,
#             PRIMARY KEY (user_id, date, hashtag)
#         )
#         ''')
#         self.conn.commit()
#         self.current_date = datetime.utcnow().strftime('%Y-%m-%d')
#         self.previous_date = (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%d')
#
#     def tearDown(self):
#         # Закрываем соединение с базой данных после каждого теста
#         self.conn.close()
#
#     def test_update_stats(self):
#         # Проверка функции update_stats
#         update_stats(1, 'user1', self.current_date, '#hashtag1')
#         self.cursor.execute('SELECT * FROM hashtag_stats')
#         rows = self.cursor.fetchall()
#         self.assertEqual(len(rows), 1)
#         self.assertEqual(rows[0], (1, 'user1', self.current_date, '#hashtag1'))
#
#     def test_get_personal_stats(self):
#         # Добавляем тестовые данные
#         update_stats(1, 'user1', self.current_date, '#hashtag1')
#         update_stats(1, 'user1', self.previous_date, '#hashtag1')
#         update_stats(1, 'user1', self.previous_date, '#hashtag2')
#
#         current_month = datetime.utcnow().strftime('%Y-%m')
#         previous_month = (datetime.utcnow().replace(day=1) - timedelta(days=1)).strftime('%Y-%m')
#
#         stats = get_stats(1, username='user1', current_month=current_month, previous_month=previous_month)
#         self.assertEqual(stats['current_month']['#hashtag1'], 1)
#         self.assertEqual(stats['previous_month']['#hashtag1'], 1)
#         self.assertEqual(stats['previous_month']['#hashtag2'], 1)
#
#     def test_get_top_users(self):
#         # Добавляем тестовые данные
#         update_stats(1, 'user1', self.current_date, '#hashtag1')
#         update_stats(2, 'user2', self.current_date, '#hashtag1')
#         update_stats(1, 'user1', self.previous_date, '#hashtag1')
#         update_stats(1, 'user1', self.previous_date, '#hashtag2')
#
#         current_month = datetime.utcnow().strftime('%Y-%m')
#         previous_month = (datetime.utcnow().replace(day=1) - timedelta(days=1)).strftime('%Y-%m')
#
#         top_users = get_top_users(current_month, previous_month)
#         self.assertEqual(len(top_users['current_month']['#hashtag1']), 2)
#         self.assertEqual(len(top_users['previous_month']['#hashtag1']), 1)
#         self.assertEqual(len(top_users['previous_month']['#hashtag2']), 1)
#
#     def test_get_monthly_report(self):
#         # Добавляем тестовые данные
#         update_stats(1, 'user1', self.previous_date, '#hashtag1')
#         update_stats(2, 'user2', self.previous_date, '#hashtag1')
#         update_stats(1, 'user1', self.previous_date, '#hashtag2')
#
#         previous_month = (datetime.utcnow().replace(day=1) - timedelta(days=1)).strftime('%Y-%m')
#
#         report = get_monthly_report(previous_month)
#         self.assertEqual(report['user1']['#hashtag1'], 1)
#         self.assertEqual(report['user2']['#hashtag1'], 1)
#         self.assertEqual(report['user1']['#hashtag2'], 1)
#
#     def test_get_yearly_report(self):
#         # Добавляем тестовые данные
#         update_stats(1, 'user1', '2024-05-02', '#hashtag1')
#         update_stats(2, 'user2', '2024-06-03', '#hashtag1')
#         update_stats(1, 'user1', '2024-07-04', '#hashtag2')
#
#         start_date = '2024-05-01'
#
#         report = get_yearly_report(start_date)
#         self.assertEqual(report['user1']['#hashtag1'], 1)
#         self.assertEqual(report['user2']['#hashtag1'], 1)
#         self.assertEqual(report['user1']['#hashtag2'], 1)
#
# if __name__ == '__test__':
#     unittest.main()
