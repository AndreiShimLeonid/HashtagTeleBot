import telebot
from datetime import datetime, timedelta
import db
import service
from check import check_message

# from db import (create_table, read_token_from_file, update_stats, get_stats, get_top_users, get_monthly_report,
#                 get_annual_report, get_users_list)

bot = telebot.TeleBot(db.read_token_from_file('token'))

if __name__ == '__main__':
    db.create_table()
    db.create_users_list()
    db.set_users_list()


# Функция для отправки файла
def send_file(chat_id, file_path):
    with open(file_path, 'r') as file:
        bot.send_document(chat_id, file)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)

    button1 = telebot.types.KeyboardButton('/stats')
    button2 = telebot.types.KeyboardButton('/top')
    button3 = telebot.types.KeyboardButton('/monthly_report')
    button4 = telebot.types.KeyboardButton('/annual_report')
    button5 = telebot.types.KeyboardButton('/download')
    markup.add(button1, button2, button3, button4, button5)
    bot.reply_to(message, "Привет! Вот доступные команды:", reply_markup=markup)


@bot.message_handler(commands=['stats'])
def send_stats(message):
    """
    Sends personal stats for current and previous months
    :param message: command /stats
    :return:
    """
    user_id = message.from_user.id
    username = message.from_user.username
    temp = f'{message.from_user.first_name} {message.from_user.last_name}'
    name = f'{message.from_user.first_name if message.from_user.last_name is None else temp}'
    current_month = datetime.fromtimestamp(message.date).strftime('%Y-%m')
    previous_month = (datetime.fromtimestamp(message.date).replace(day=1) - timedelta(days=1)).strftime('%Y-%m')
    response = db.get_stats(user_id, username, name, current_month, previous_month)

    if response[0] == 0:
        bot.reply_to(message, "У вас нет упоминаний отслеживаемых хештегов.",
                     reply_markup=telebot.types.ReplyKeyboardRemove())
        return
    else:
        bot.reply_to(message, response[1],
                     reply_markup=telebot.types.ReplyKeyboardRemove())


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

    top_users = db.get_top_users(current_month, previous_month)

    response = f"Топ 5 кордонцев по хештегам:\n"

    for month in [service.format_month(current_month), service.format_month(previous_month)]:
        response += f'\n {month}\n'
        for hashtag, users in top_users[month].items():
            response += f"\n  {hashtag}:\n"
            i = 0
            for username, count in users:
                i += 1
                response += f"   {i}. {username}: {count}\n"

    bot.reply_to(message, response,
                 reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=['users'])
def send_users_list(message):
    """
    Sends users list
    :param message: command /users
    :return:
    """
    response = ''
    users = db.get_users_list()
    for user in users:
        response += f'{user}\n'
    bot.reply_to(message, response,
                 reply_markup=telebot.types.ReplyKeyboardRemove())


# Команда для получения подробной статистики всех пользователей за прошедший месяц
@bot.message_handler(commands=['monthly_report'])
def send_monthly_report(message):
    """
    Sends all users statistics for current and previous months
    :param message: command /monthly_stats
    :return:
    """
    current_month = datetime.now().strftime('%Y-%m')
    previous_month = (datetime.fromtimestamp(message.date).replace(day=1) - timedelta(days=1)).strftime('%Y-%m')
    response = ''

    def create_response(report, month):
        result = f"Подробная статистика за {service.format_month(month)}:\n"
        for username, hashtags in report.items():
            result += f"\n{username}:\n"
            for hashtag, count in hashtags.items():
                result += f"  {hashtag}: {count}\n"
        return result
    for month in [current_month, previous_month]:
        response += f'{create_response(db.get_monthly_report(month), month)}'
    bot.reply_to(message, response,
                 reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=['annual_report'])
def send_annual_report(message):
    """
    Send report from start date till now
    :param message: command /yearly_report
    :return:
    """
    today = datetime.now().strftime('%Y-%m-%d')

    report = db.get_annual_report(db.start_date)

    response = f"Общие итоги с {service.format_date(db.start_date)} по {service.format_date(today)}:\n"

    for username, hashtags in report.items():
        response += f"\n{username}:\n"
        for hashtag, count in hashtags.items():
            response += f"  {hashtag}: {count}\n"

    bot.reply_to(message, response,
                 reply_markup=telebot.types.ReplyKeyboardRemove())


# Обработчик команды /download
@bot.message_handler(commands=['download'])
def handle_download(message):
    db.export_report()
    send_file(message.chat.id, db.report_file_path)
    bot.reply_to(message, "Таблица с отметками во вложении.",
                 reply_markup=telebot.types.ReplyKeyboardRemove())


# Обработчик команды /download
@bot.message_handler(commands=['users'])
def handle_download(message):
    db.export_users()
    send_file(message.chat.id, db.users_export_path)
    bot.reply_to(message, "Таблица с пользователями во вложении.")


@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'document', 'animation'])
def handle_message(message):
    user_id = message.from_user.id
    username = message.from_user.username
    temp = f'{message.from_user.first_name} {message.from_user.last_name}'
    name = f'{message.from_user.first_name if message.from_user.last_name is None else temp}'
    text = message.caption if message.text is None else message.text
    if text is not None:
        # Сдвинутое время на 7 часов назад для учёта ночных (до 7 утра) отметок
        time_shift = 7
        shifted_date = (datetime.fromtimestamp(message.date) - timedelta(hours=time_shift))
        date = datetime.fromtimestamp(message.date)

        code, response, hashtag = check_message(text, db.TRACKED_HASHTAGS, message.content_type, username, user_id)
        if code == 0:
            bot.reply_to(message, response)
            bot.send_message(db.admin_id, f'!!! Не засчитан - отсутствует доказательство к хештегу\n'
                                          f'Content type: {message.content_type}\n'
                                          f'ID: {user_id}, Name: "{name}", Username: "{username}", hashtag: "{hashtag}"')
        elif code == 1:
            if not db.update_stats(user_id, username, name, shifted_date.date(), hashtag):
                bot.send_message(db.admin_id,
                                 f'!!! Не засчитан - Повторный пост\n'
                                 f'Content type: {message.content_type}\n'
                                 f'ID: {user_id}, Name: "{name}", Username: "{username}", hashtag: "{hashtag}"')
                # response = 'Похвально! Но отметка за сегодня уже была 😊'
            else:
                bot.send_message(db.admin_id, f'Пост засчитан\n'
                                              f'Content type: {message.content_type}\n'
                                              f'Date: {date.strftime("%d/%m/%Y, %H:%M")} -> '
                                              f'goes as {shifted_date.strftime("%d/%m/%Y, %H:%M")}\n'
                                              f'ID: {user_id}, Name: "{name}", Username: "{username}", hashtag: "{hashtag}"')
                # bot.reply_to(message, response)


bot.polling(non_stop=True)
