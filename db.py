import sqlite3

def read_token_from_file(file:str):
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
        year INTEGER,
        month TEXT,
        hashtag TEXT,
        count INTEGER,
        PRIMARY KEY (user_id, year, month, hashtag)
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()


def update_stats(user_id, username, year, month, hashtag):
    conn = sqlite3.connect('hashtag_stats.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO hashtag_stats (user_id, username, year, month, hashtag, count)
    VALUES (?, ?, ?, ?, ?, ?)
    ON CONFLICT(user_id, year, month, hashtag)
    DO UPDATE SET count = count + 1
    ''', (user_id, username, year, month, hashtag, 1))
    conn.commit()
    cursor.close()
    conn.close()


def get_stats(user_id, username):
    conn = sqlite3.connect('hashtag_stats.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT year, month, hashtag, count FROM hashtag_stats
    WHERE user_id = ?
    ''', (user_id,))

    rows = cursor.fetchall()
    if not rows:
        cursor.close()
        conn.close()
        return [0, "У вас нет упоминаний отслеживаемых хештегов."]

    response = f"Статистика для пользователя @{username}:\n"

    stats = {}
    for row in rows:
        year, month, hashtag, count = row
        if year not in stats:
            stats[year] = {}
        if month not in stats[year]:
            stats[year][month] = {}
        stats[year][month][hashtag] = count

    for year in sorted(stats.keys()):
        response += f"\n{year}:\n"
        for month in sorted(stats[year].keys()):
            response += f"  {month}:\n"
            for hashtag, count in stats[year][month].items():
                response += f"    {hashtag}: {count}\n"

    cursor.close()
    conn.close()
    return [1, response]