import json
import sqlite3
import service

log_file = 'log.txt'
report_file_path = 'report.txt'
users_export_path = 'users_export.txt'
users_file_name = 'user_info.txt'
stats_db_name = 'hashtag_stats.db'
start_date = '2024-05-01'
TRACKED_HASHTAGS = ['#добрый', '#недобрый']
admin_id = 1357737507


def delete_row_from_db(row_id: int):
    conn = sqlite3.connect(stats_db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM hashtag_stats WHERE id = ?
    ''', (row_id,))
    if cursor.rowcount == 0:
        service.log_write(f"db.delete_row_from_db() -> row id:{row_id} deletion failed.")
        conn.commit()
        cursor.close()
        conn.close()
        return False
    else:
        service.log_write(f"db.delete_row_from_db() -> row id:{row_id} deletion completed.")
        conn.commit()
        cursor.close()
        conn.close()
        return True


def create_users_list():
    conn = sqlite3.connect(stats_db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            username TEXT,
            UNIQUE(user_id)
        )
        ''')
    cursor.close()
    conn.close()


def set_users_list():
    with open(users_file_name, 'r') as file:
        users = file.readlines()
    conn = sqlite3.connect(stats_db_name, check_same_thread=False)
    cursor = conn.cursor()
    for line in users:
        user = json.loads(line)
        user_id, username = user.get('id'), user.get(
            'username')
        name = f"{user.get('first_name') if user.get('last_name') is None else user.get(
            'first_name') + ' ' + user.get('last_name')}"
        cursor.execute('''
        INSERT INTO users_list (user_id, username, name)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id)
        DO NOTHING
        ''', (user_id, username, name))
    if cursor.rowcount == 0:
        service.log_write(f"db.set_users_list() -> Failed to update users list. "
                          f"No lines inserted from '{users_file_name}'.")
    else:
        service.log_write(f"db.set_users_list() -> The users table has been updated from '{users_file_name}'.")
    conn.commit()
    cursor.close()
    conn.close()


def get_user_info(user_id: int):
    """
    Returns user info (name, username) from the table users_list (hashtag_stats.db)
    :param user_id: unique user id - int
    :return: name, username
    """
    conn = sqlite3.connect(stats_db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT name, username FROM users_list
    WHERE user_id = ?
    ''', (user_id,))
    user_info = cursor.fetchone()
    if user_info is None:
        service.log_write(f"db.get_user_info(user_id: int) -> There is no info about user with id:{user_id} .")
        cursor.close()
        conn.close()
        return None, None
    else:
        service.log_write(f"db.get_user_info(user_id: int) -> returned user info with id:{user_id}.")
        cursor.close()
        conn.close()
        name, username = user_info
        return name.replace('None', '').strip(), username


def export_users():
    conn = sqlite3.connect(stats_db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM users_list
    ''', )
    rows = cursor.fetchall()

    if rows:
        with open(users_export_path, 'w') as f:
            f.writelines('N, user_id, name, username\n')
            for row in rows:
                line = ', '.join(map(str, row))
                f.writelines(f'{line}\n')
    else:
        with open(users_export_path, 'w') as f:
            f.writelines('N, user_id, name, username\n')
    service.log_write(f"db.export_report() -> the users file has been created.")
    cursor.close()
    conn.close()


def export_report():
    conn = sqlite3.connect(stats_db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM hashtag_stats
    ''', )
    rows = cursor.fetchall()

    if rows:
        with open(report_file_path, 'w') as f:
            f.writelines('N, user_id, name, username, date, hashtag\n')
            for row in rows:
                line = ', '.join(map(str, row))
                f.writelines(f'{line}\n')
    else:
        with open(report_file_path, 'w') as f:
            f.writelines('N, user_id, name, username, date, hashtag\n')
    service.log_write(f"db.export_report() -> the report file has been updated.")
    cursor.close()
    conn.close()


def get_users_list():
    """
    This method export users list from the db
    :return: users list from db table users_list
    """
    conn = sqlite3.connect(stats_db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users_list
        ''')
    users = cursor.fetchall()
    result = []
    if not users:
        service.log_write(f"db.get_users_list() -> the users table is empty.")
    else:
        for user in users:
            result.append(user)
        service.log_write(f"db.get_users_list() -> Success.")
    return result


def add_user(user_id, name, username=None):
    """
    This method performs the addition of new user to the user table in db.
    :param name: user first name and last name
    :param user_id: unique int user id, None by default
    :param username: username, None by default
    :return: False if the username/user_id is already in the users list
            True if the username/user_id has been added to the users list
    """
    conn = sqlite3.connect(stats_db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users_list (user_id, username, name)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id)
        DO NOTHING
        ''', (user_id, username, name))
    if cursor.rowcount == 0:
        service.log_write(f"db.add_user() -> Failed to add user to the list. Conflict by id occurred ID:'{user_id}'.")
        conn.commit()
        cursor.close()
        conn.close()
        return False
    service.log_write(f"db.add_user() -> New user has benn added to the list. ID:'{user_id}'.")
    conn.commit()
    cursor.close()
    conn.close()
    return True


def remove_user(user_id):
    """
    This method performs the deletion of the user from the user list.
    :return: False if the username is not in the users list
            True if the username has been deleted from the users list
    """
    conn = sqlite3.connect(stats_db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM users_list WHERE user_id = ?
    ''', (user_id,))
    if cursor.rowcount == 0:
        service.log_write(f"db.remove_user() -> Failed to remove. There is no user with ID:'{user_id}'.")
        conn.commit()
        cursor.close()
        conn.close()
        return False
    else:
        service.log_write(f"db.remove_user() -> The user has been removed from the list. ID:'{user_id}'.")
    conn.commit()
    cursor.close()
    conn.close()
    return True


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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hashtag_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            username TEXT,
            date TEXT,
            hashtag TEXT,
            UNIQUE(user_id, date, hashtag)
        )
        ''')
    conn.commit()
    cursor.close()
    conn.close()


def update_stats(user_id, username, name, date, hashtag):
    """
    Method performs the addition of a new user to the database table
    :param name: user first name and last name
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
    INSERT INTO hashtag_stats (user_id, username, name, date, hashtag)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(user_id, date, hashtag)
    DO NOTHING
    ''', (user_id, username, name, date, hashtag))
    if cursor.rowcount == 0:
        service.log_write(f"Conflict occurred: The row {user_id, username, name, date, hashtag} already exists.")
        conn.commit()
        cursor.close()
        conn.close()
        return False

    service.log_write(f"Row {user_id, username, name, date, hashtag} inserted successfully.")
    conn.commit()
    cursor.close()
    conn.close()
    return True


def get_stats(user_id, username, name, current_month, previous_month):
    """
    Method gets user's stats from the database table with users' statistics
    :param name: user first name and last name (if not None)
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

    response = f"Статистика для пользователя {name}:\n" if username is None else (f"Статистика "
                                                                                  f"для пользователя @{username}:\n")

    for month in ['current_month', 'previous_month']:
        if stats[month]:  # проверяем, пустой ли словарь внутри месяца
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
    SELECT user_id, hashtag, strftime('%Y-%m', date) as month, COUNT(*) as count 
    FROM hashtag_stats
    WHERE strftime('%Y-%m', date) = ? OR strftime('%Y-%m', date) = ?
    GROUP BY user_id, hashtag, month
    ORDER BY month, count DESC
    ''', (current_month, previous_month))

    rows = cursor.fetchall()
    current_month_formatted = service.format_month(current_month)
    previous_month_formatted = service.format_month(previous_month)
    top_users = {current_month_formatted: {}, previous_month_formatted: {}}

    for row in rows:
        user_id, hashtag, month, count = row
        name, username = get_user_info(user_id)
        period = current_month_formatted if month == current_month else previous_month_formatted
        if hashtag not in top_users[period]:
            top_users[period][hashtag] = []
        if len(top_users[period][hashtag]) < 5:
            if username is None:
                top_users[period][hashtag].append((name, count))
            else:
                top_users[period][hashtag].append((f'@{username}', count))

    cursor.close()
    conn.close()
    return top_users


# Функция для получения подробной статистики всех пользователей за прошедший месяц
def get_monthly_report(month):
    """
    This method shows hashtags statistics for previous month
    :param month: month
    :return: str previous month statistics
    """
    conn = sqlite3.connect(stats_db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT user_id, hashtag, COUNT(*) as count 
    FROM hashtag_stats
    WHERE strftime('%Y-%m', date) = ?
    GROUP BY user_id, hashtag
    ORDER BY hashtag
    ''', (month,))

    rows = cursor.fetchall()

    report = {}

    for row in rows:
        user_id, hashtag, count = row
        name, username = get_user_info(user_id)
        key = f'@{username}' if username else f'{name}'
        if key not in report:
            report[key] = {}
        report[key][hashtag] = count
    cursor.close()
    conn.close()
    return report


# Функция для получения общих итогов с 1 мая 2024 года по текущую дату
def get_annual_report(start_date):
    """
    Shows statistics from start_date till now
    :param start_date: format YYYY-MM-DD
    :return: str report from start date
    """
    conn = sqlite3.connect(stats_db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT user_id, hashtag, COUNT(*) as count 
    FROM hashtag_stats
    WHERE date >= ?
    GROUP BY user_id, hashtag
    ORDER BY user_id, hashtag
    ''', (start_date,))

    rows = cursor.fetchall()

    report = {}

    for row in rows:
        user_id, hashtag, count = row
        name, username = get_user_info(user_id)
        key = f'@{username}' if username else f'{name}'
        if key not in report:
            report[key] = {}
        report[key][hashtag] = count

    cursor.close()
    conn.close()
    return report
