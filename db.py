import sqlite3

users_file_name = 'users.txt'
stats_db_name = 'hashtag_stats.db'


def get_users_list():
    """
    This method reads file with users
    :return: users list if the file exists
            0 if the file doesn't exist
    """
    users = []
    try:
        with open(users_file_name, 'r') as file:
            for line in file:
                line = line.rstrip()
                # Печать строки (или обработка строки по вашему усмотрению)
                users.append(line)
        print('allowed users: ', *users)
        return users
    except FileNotFoundError:
        with open(users_file_name, 'w'):
            pass
        print(f'File {users_file_name} has not been found. New file has been created')
        return 0


def add_user(username: str):
    """
    This method performs the addition of new user to the user list.
    :param username: username, example: @username
    :return: 0 if the username is already in the users list
            1 if the username has been added to the users list
            -1 if the username type is not string, '@' is absent and the length is less or equal 1
    """
    if type(username) is str and '@' in username and len(username) > 1:
        if username in get_users_list():
            print(f'user {username} is already in the users list')
            return 0
        else:
            with open(users_file_name, 'a') as file:
                file.write(f'{username}\n')
                print(f'user {username} has been added to the users list')
                return 1
    else:
        print(f'wrong username {username}')
        return -1


def remove_user(username: str):
    """
    This method performs the deletion of the user from the user list.
    :param username: username, example: @username
    :return: 0 if the username is not in the users list
            1 if the username has been deleted from the users list
            -1 if the username type is not string, '@' is absent and the length is less or equal 1
    """
    if type(username) is str and '@' in username and len(username) > 1:
        users = get_users_list()
        if username in users:
            with open(users_file_name, 'r') as file:
                lines = file.readlines()
            with open(users_file_name, 'w') as file:
                for line in lines:
                    if line.rstrip() != username:
                        file.write(line.rstrip() + '\n')
            print(f'user {username} has been deleted from the users list')
            return 1
        else:
            print(f'failed to find {username} in the users list')
            return 0
    else:
        print(f'wrong username {username}')
        return -1


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
    :return:
    """
    conn = sqlite3.connect(stats_db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO hashtag_stats (user_id, username, date, hashtag)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(user_id, username, date, hashtag)
    DO NOTHING
    ''', (user_id, username, date, hashtag))
    conn.commit()
    cursor.close()
    conn.close()


def get_stats(user_id, username, current_month, previous_month):
    """
    Method gets user's stats from the database table with users' statistics
    :param user_id: int
    :param username: format @username
    :param current_month: format YYYY-MM
    :param previous_month: format YYYY-MM
    :return: [0, alert: str] if there is no any statistics for the user within 2 last months
            [1, statistics: str] if there is any statistics for the user within 2 last months
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
        response += f"\n{'Текущий месяц' if month == 'current_month' else 'Прошлый месяц'}:\n"
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

    top_users = {'current_month': {}, 'previous_month': {}}

    for row in rows:
        username, hashtag, month, count = row
        period = 'current_month' if month == current_month else 'previous_month'
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
