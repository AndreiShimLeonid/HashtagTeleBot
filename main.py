import telebot
from datetime import datetime, timedelta

import service
from check import check_message
from db import create_table, read_token_from_file, update_stats, get_stats, get_top_users, get_monthly_report, get_yearly_report

bot = telebot.TeleBot(read_token_from_file('token'))
TRACKED_HASHTAGS = ['#добрый', '#недобрый']
start_date = '2024-05-01'

if __name__ == '__main__':
    create_table()


@bot.message_handler(commands=['stats'])
def send_stats(message):
    """
    Sends personal stats for current and previous months
    :param message: command /stats
    :return:
    """
    user_id = message.from_user.id
    username = message.from_user.username
    current_month = datetime.fromtimestamp(message.date).strftime('%Y-%m')
    previous_month = (datetime.fromtimestamp(message.date).replace(day=1) - timedelta(days=1)).strftime('%Y-%m')
    response = get_stats(user_id, username, current_month, previous_month)

    if response[0] == 0:
        bot.reply_to(message, "У вас нет упоминаний отслеживаемых хештегов.")
        return
    else:
        bot.reply_to(message, response[1])


# Команда для получения топ 5 пользователей
@bot.message_handler(commands=['top'])
def send_top_users(message):
    """
    Sends top 5 users stats for current and previous months
    :param message: command /top
    :return:
    """
    current_month = datetime.fromtimestamp(message.date).strftime('%Y-%m')
    previous_month = (datetime.fromtimestamp(message.date).replace(day=1) - timedelta(days=1)).strftime('%Y-%m')

    top_users = get_top_users(current_month, previous_month)

    response = f"Топ 5 пользователей по хештегам:\n"

    for month in [service.format_month(current_month), service.format_month(previous_month)]:
        # response += f"\n{'Текущий месяц' if month == 'current_month' else 'Прошлый месяц'}:\n"
        response += f'\n {month}\n'
        for hashtag, users in top_users[month].items():
            response += f"\n  {hashtag}:\n"
            for username, count in users:
                response += f"    @{username}: {count}\n"

    bot.reply_to(message, response)


# Команда для получения подробной статистики всех пользователей за прошедший месяц
@bot.message_handler(commands=['monthly_report'])
def send_monthly_report(message):
    """
    Sends all users statistics for current and previous months
    :param message: command /monthly_stats
    :return:
    """
    previous_month = (datetime.fromtimestamp(message.date).replace(day=1) - timedelta(days=1)).strftime('%Y-%m')
    report = get_monthly_report(previous_month)

    response = f"Подробная статистика за прошедший месяц:\n"

    for username, hashtags in report.items():
        response += f"\n@{username}:\n"
        for hashtag, count in hashtags.items():
            response += f"  {hashtag}: {count}\n"

    bot.reply_to(message, response)


@bot.message_handler(commands=['yearly_report'])
def send_yearly_report(message):
    """
    Send report from start date till now
    :param message: command /yearly_report
    :return:
    """
    global start_date

    report = get_yearly_report(start_date)

    response = f"Общие итоги с 1 мая 2024 года по текущую дату:\n"

    for username, hashtags in report.items():
        response += f"\n@{username}:\n"
        for hashtag, count in hashtags.items():
            response += f"  {hashtag}: {count}\n"

    bot.reply_to(message, response)


@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'document'])
def handle_message(message):
    user_id = message.from_user.id
    username = message.from_user.username
    text = message.caption if message.text is None else message.text
    if text is not None:
        date = datetime.fromtimestamp(message.date).date()

        code, response, hashtag = check_message(text, TRACKED_HASHTAGS, message.content_type, username)
        if code == 0:
            bot.reply_to(message, response)
        elif code == 1:
            if not update_stats(user_id, username, date, hashtag):
                response = 'Похвально! Но отметка за сегодня уже была 😊'
            bot.reply_to(message, response)


bot.polling(non_stop=True)
