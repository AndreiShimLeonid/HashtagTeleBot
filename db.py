import sqlite3


def read_token_from_file(file: str):
    with open(file, 'r') as file:
        # Чтение одной строки из файла
        return file.readline()


def create_table():
    conn = sqlite3.connect('hashtag_stats.db', check_same_thread=False)
    cursor = conn.cursor()
    # Создание таблицы для хранения статистики
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hashtag_stats (
        user_id INTEGER,
        username TEXT,
        date TEXT,
        hashtag TEXT,
        PRIMARY KEY (user_id, date, hashtag)
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()


def update_stats(user_id, username, date, hashtag):
    conn = sqlite3.connect('hashtag_stats.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO hashtag_stats (user_id, username, date, hashtag)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(user_id, date, hashtag)
    DO NOTHING
    ''', (user_id, username, date, hashtag))
    conn.commit()
    cursor.close()
    conn.close()


def get_stats(user_id, username, current_month, previous_month):
    conn = sqlite3.connect('hashtag_stats.db', check_same_thread=False)
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
    conn = sqlite3.connect('hashtag_stats.db', check_same_thread=False)
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
    conn = sqlite3.connect('hashtag_stats.db', check_same_thread=False)
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
