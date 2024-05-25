import json
import os
import sqlite3

import service

users_file_name = 'user_info.txt'
stats_db_name = 'hashtag_stats.db'


def get_users_list():
    """
    This method reads file with users
    :return: users list if the file exists
            0 if the file doesn't exist
    """
    users = []
    if not os.path.exists(users_file_name):
        with open(users_file_name, 'w'):
            pass
        print(f'File {users_file_name} has not been found. New file has been created')
        return 0
    with open(users_file_name, 'r', encoding='utf-8') as f:
        for line in f:
            user_info = json.loads(line)
            users.append(f"ID: {user_info['id']} "
                         f"Username: {user_info['username']} "
                         f"Name: {user_info['first_name']} {user_info['last_name']}\n")
        print('allowed users: \n', *users)
        return users


def user_exists(id: int, username: str):
    """
    Checks if user exists
    :param id: int
    :param username: string
    :return: True if user exists in the file
            False if file doesn't exist or user doesn't exist in the file
    """
    if not os.path.exists(users_file_name):
        return False
    with open(users_file_name, 'r', encoding='utf-8') as f:
        for line in f:
            user_info = json.loads(line)
            if (user_info['id'] == id and user_info['id'] is not None) or (
                    user_info['username'] == username and user_info['username'] is not None):
                return True
    return False


def add_user(user_id=None, first_name=None, last_name=None, username=None, language_code=None, is_bot=None):
    """
    This method performs the addition of new user to the user list.
    :param user_id: unique int user id, None by default
    :param language_code: ru, None by default
    :param is_bot: false/true, None by default
    :param last_name: string, None by default
    :param first_name: string, None by default
    :param username: username, None by default
    :return: 0 if the username/user_id is already in the users list
            1 if the username/user_id has been added to the users list
            -1 if the username/user_id both are None
    """
    if user_id is None and username is None:
        print(f'wrong username {username} and id {user_id}')
        return -1
    if user_exists(user_id, username):
        print(f"User with ID {user_id} or username {username} already exists.")
        return 0
    user_info = {
        'id': user_id,
        'first_name': first_name,
        'last_name': last_name,
        'username': username,
        'language_code': language_code,
        'is_bot': is_bot
    }
    with open(users_file_name, 'a', encoding='utf-8') as f:
        f.write(json.dumps(user_info, ensure_ascii=False) + '\n')
    print(f"Saved user with ID {user_id} and username {username}.")
    return 1


def remove_user(user_id, username):
    """
    This method performs the deletion of the user from the user list.
    :param username: username, example: username
    :return: False if the username is not in the users list
            True if the username has been deleted from the users list
    """
    if user_exists(user_id, username):
        users = []
        with open(users_file_name, 'r', encoding='utf-8') as f:
            for line in f:
                users.append(json.loads(line))
        with open(users_file_name, 'w', encoding='utf-8') as f:
            for user in users:
                if user['id'] != user_id or user['username'] != username:
                    f.write(json.dumps(user, ensure_ascii=False) + '\n')
            print(f'User {username} with id {user_id} has been deleted from the users list')
            return True
    print(f'Failed to find {username} in the users list')
    return False


def read_token_from_file(file: str):
    """
    reads token from file
    :param file: file name
    :return: str
    """
    with open(file, 'r') as file:
        # Чтение одной строки из файла
        return file.readline()


def create_table():
    """
    Method creates table in the database
    :return: nothing
    """
    conn = sqlite3.connect(stats_db_name, check_same_thread=False)
    cursor = conn.cursor()
    # Создание таблицы для хранения статистики
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hashtag_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            date TEXT,
            hashtag TEXT,
            UNIQUE(user_id, username, date, hashtag)
        )
        ''')
    conn.commit()
    cursor.close()
    conn.close()


def update_stats(user_id, username, date, hashtag):
    """
    Method performs the addition of a new user to the database table
    :param user_id: int
    :param username: format @username
    :param date: format YYYY-MM-DD
    :param hashtag: format #hashtag
    :return: True - if stats have been updated
            False - if stats haven't been updated because a conflict on user, date and hashtag has occurred
    """
    conn = sqlite3.connect(stats_db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO hashtag_stats (user_id, username, date, hashtag)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(user_id, username, date, hashtag)
    DO NOTHING
    ''', (user_id, username, date, hashtag))
    if cursor.rowcount == 0:
        print(f"Conflict occurred: The row {user_id, username, date, hashtag} already exists.")
        conn.commit()
        cursor.close()
        conn.close()
        return False

    print(f"Row {user_id, username, date, hashtag} inserted successfully.")
    conn.commit()
    cursor.close()
    conn.close()
    return True


def get_stats(user_id, username, current_month, previous_month):
    """
    Method gets user's stats from the database table with users' statistics
    :param user_id: int
    :param username: format @username
    :param current_month: format YYYY-MM
    :param previous_month: format YYYY-MM
    :return: [0, alert] if there is no any statistics for the user within 2 last months
            [1, statistics] if there is any statistics for the user within 2 last months
    """
    conn = sqlite3.connect(stats_db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT hashtag, date FROM hashtag_stats
    WHERE user_id = ? AND (strftime('%Y-%m', date) = ? OR strftime('%Y-%m', date) = ?)
    ''', (user_id, current_month, previous_month))

    rows = cursor.fetchall()
    stats = {'current_month': {}, 'previous_month': {}}
    if not rows:
        cursor.close()
        conn.close()
        return [0, "У вас нет упоминаний отслеживаемых хештегов."]

    for row in rows:
        hashtag, date = row
        month = 'current_month' if date.startswith(current_month) else 'previous_month'
        if hashtag not in stats[month]:
            stats[month][hashtag] = 0
        stats[month][hashtag] += 1

    response = f"Статистика для пользователя @{username}:\n"

    for month in ['current_month', 'previous_month']:
        if stats[month]:  #проверяем, пустой ли словарь внутри месяца
            response += f"\n{service.format_month(current_month) if month == 'current_month' else service.format_month(previous_month)}:\n"
            for hashtag, count in stats[month].items():
                response += f"  {hashtag}: {count}\n"

    cursor.close()
    conn.close()
    return [1, response]


# Функция для получения топ 5 пользователей по хештегам за текущий и прошлый месяцы
def get_top_users(current_month, previous_month):
    """
    Method shows top 5 users by hashtags count within two months
    :param current_month: format yyyy-mm
    :param previous_month: format yyyy-mm
    :return: str top 5 users info
    """
    conn = sqlite3.connect(stats_db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT username, hashtag, strftime('%Y-%m', date) as month, COUNT(*) as count 
    FROM hashtag_stats
    WHERE strftime('%Y-%m', date) = ? OR strftime('%Y-%m', date) = ?
    GROUP BY username, hashtag, month
    ORDER BY month, count DESC
    ''', (current_month, previous_month))

    rows = cursor.fetchall()
    current_month_formatted = service.format_month(current_month)
    previous_month_formatted = service.format_month(previous_month)
    top_users = {current_month_formatted: {}, previous_month_formatted: {}}

    for row in rows:
        username, hashtag, month, count = row
        period = current_month_formatted if month == current_month else previous_month_formatted
        if hashtag not in top_users[period]:
            top_users[period][hashtag] = []
        if len(top_users[period][hashtag]) < 5:
            top_users[period][hashtag].append((username, count))

    cursor.close()
    conn.close()
    return top_users


# Функция для получения подробной статистики всех пользователей за прошедший месяц
def get_monthly_report(previous_month):
    """
    This method shows hashtags statistics for previous month
    :param previous_month: format YYYY-MM
    :return: str previous month statistics
    """
    conn = sqlite3.connect(stats_db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT username, hashtag, COUNT(*) as count 
    FROM hashtag_stats
    WHERE strftime('%Y-%m', date) = ?
    GROUP BY username, hashtag
    ORDER BY username, hashtag
    ''', (previous_month,))

    rows = cursor.fetchall()

    report = {}

    for row in rows:
        username, hashtag, count = row
        if username not in report:
            report[username] = {}
        report[username][hashtag] = count

    cursor.close()
    conn.close()
    return report


# Функция для получения общих итогов с 1 мая 2024 года по текущую дату
def get_yearly_report(start_date):
    """
    Shows statistics from start_date till now
    :param start_date: format YYYY-MM-DD
    :return: str report from start date
    """
    conn = sqlite3.connect(stats_db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT username, hashtag, COUNT(*) as count 
    FROM hashtag_stats
    WHERE date >= ?
    GROUP BY username, hashtag
    ORDER BY username, hashtag
    ''', (start_date,))

    rows = cursor.fetchall()

    report = {}

    for row in rows:
        username, hashtag, count = row
        if username not in report:
            report[username] = {}
        report[username][hashtag] = count

    cursor.close()
    conn.close()
    return report
