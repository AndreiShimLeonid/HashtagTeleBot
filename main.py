import telebot
import sqlite3
import datetime

from check import check_message
from db import create_table, read_token_from_file, update_stats, get_stats

bot = telebot.TeleBot(read_token_from_file('token'))
TRACKED_HASHTAGS = ['#добрый', '#недобрый']

if __name__ == ('__main__'):
    create_table()


# Функция для обновления статистики в базе данных



@bot.message_handler(commands=['stats'])
def send_stats(message):
    user_id = message.from_user.id
    username = message.from_user.username
    response = get_stats(user_id, username)

    if response[0] == 0:
        bot.reply_to(message, "У вас нет упоминаний отслеживаемых хештегов.")
        return
    else:
        bot.reply_to(message, response[1])


@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'document'])
def handle_message(message):
    user_id = message.from_user.id
    username = message.from_user.username
    text = message.text
    if text is None:
        text = message.caption
    date = message.date
    dt = datetime.datetime.fromtimestamp(date)
    year = dt.year
    month = dt.strftime('%B')
    try:
        code, response, hashtag = check_message(text, TRACKED_HASHTAGS, message.content_type, username)
        if code == 0:
            bot.reply_to(message, response)
        else:
            update_stats(user_id, username, year, month, hashtag)
            bot.reply_to(message, response)
    except:
        print("no hashtag")

bot.polling(non_stop=True)
