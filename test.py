import datetime
import json
import unittest
import sqlite3
import random
from datetime import datetime, timedelta

import db
from db import update_stats, get_stats, get_top_users, get_monthly_report, get_annual_report
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


def random_date(start_date, end_date):
    # Преобразуем строки дат в объекты datetime
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')

    # Вычисляем разницу в днях между датами
    delta = end_dt - start_dt

    # Выбираем случайное количество дней в этом диапазоне
    random_days = random.randint(0, delta.days)

    # Добавляем случайное количество дней к начальной дате
    random_dt = start_dt + timedelta(days=random_days)

    # Преобразуем результат обратно в строку формата yyyy-mm-dd
    return random_dt.strftime('%Y-%m-%d')


# Пример использования
start_date = '2024-04-01'
end_date = '2024-05-31'


def random_user(users_file_name):
    users = []
    with open(users_file_name, 'r', encoding='utf-8') as f:
        for line in f:
            user = json.loads(line)
            temp = f'{user['first_name']} {user['last_name']}'
            name = f'{user['first_name'] if user['last_name'] is None else temp}'
            users.append([user['id'], user['username'], name])
    return random.choice(users)

hashtags = ['#добрый', '#недобрый']
for i in range(500):
    user = random_user('user_info.txt')
    update_stats(user_id=user[0], username=user[1], name=user[2], date=random_date(start_date,end_date), hashtag=random.choice(hashtags))

# {"id": 1357737507, "first_name": "Andrei", "last_name": "Shim", "username": "shimandrei", "language_code": "ru", "is_bot": false}
update_stats(1357737507, 'shimandrei', 'Andrei Shim', '2024-04-30', '#добрый')
# print(get_stats(user_id=818537230, username='katess8', name='Ekaterina Katess8', current_month='2024-05', previous_month='2024-04'))
# print(get_stats(user_id=336055079, username='Sergey_aka_Nikola', name='Сергей Никольский', current_month='2024-05', previous_month='2024-04'))
# print(get_stats(user_id=2050825648, username=None, name='Евгений Андреев', current_month='2024-05', previous_month='2024-04'))
#
# for i in range(100):
#     user = random_user('user_info.txt')
#     print(get_stats(user_id=user[0], username=user[1], name=user[2], current_month='2024-05', previous_month='2024-04'))


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
