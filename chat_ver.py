import telebot
import sqlite3
import datetime


def read_token_from_file():
    with open('token', 'r') as file:
        # Чтение одной строки из файла
        return file.readline()


bot = telebot.TeleBot(read_token_from_file())


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


# Хештеги для отслеживания
TRACKED_HASHTAGS = ['#добрый', '#недобрый']

if __name__ == '__chat_ver__':
    create_table()


# Функция для обновления статистики в базе данных
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


@bot.message_handler(commands=['stats'])
def send_stats(message):
    user_id = message.from_user.id
    username = message.from_user.username
    conn = sqlite3.connect('hashtag_stats.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT year, month, hashtag, count FROM hashtag_stats
    WHERE user_id = ?
    ''', (user_id,))

    rows = cursor.fetchall()

    if not rows:
        bot.reply_to(message, "У вас нет упоминаний отслеживаемых хештегов.")
        return

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

    bot.reply_to(message, response)
    cursor.close()
    conn.close()
    # Обработчик сообщений


@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'document'])
def handle_message(message):
    user_id = message.from_user.id
    username = message.from_user.username
    text = message.text
    if text == None:
        text = message.caption
    date = message.date
    # dt = datetime.utcfromtimestamp(date)
    dt = datetime.datetime.fromtimestamp(date)
    year = dt.year
    month = dt.strftime('%B')

    # Проверка наличия отслеживаемых хештегов в сообщении
    for hashtag in TRACKED_HASHTAGS:
        if hashtag in text.split():
            if message.content_type == "text":
                bot.reply_to(message, "Не верю. Где ваши доказательства?")
                # TODO сделать функцию для логирования
                print(datetime.datetime.now(),
                      f'-- Failed to update database - no picture with hashtag from @{username}')
            else:
                update_stats(user_id, username, year, month, hashtag)
                bot.reply_to(message, "👍")
                print(datetime.datetime.now(), f'-- DB is updated - visual content with hashtag from @{username}')


# Команда для получения статистики

# Запуск бота
bot.polling(non_stop=True)
