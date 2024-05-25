import os
from datetime import datetime

import telebot, json, db, check, service

# Укажите ваш токен API, выданный BotFather
bot = telebot.TeleBot(db.read_token_from_file('token'))


def check_message(text, tracked_hashtags, content_type, username):
    # Пример реализации функции
    for hashtag in tracked_hashtags:
        if hashtag in text:
            return 1, f"Отлично, {username}! Вы использовали хэштег {hashtag}", hashtag
    return 0, "Сообщение не содержит отслеживаемых хэштегов", None


# Обработчик всех сообщений
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'document'])
def handle_message(message):
    if message.forward_from:
        user_id = message.forward_from.id
        username = message.forward_from.username
        first_name = message.forward_from.first_name or ""
        last_name = message.forward_from.last_name or ""
        name = f"{first_name} {last_name}".strip()

        # Инициализация переменных
        text = None
        content_type = message.content_type

        # Получение текста сообщения
        if content_type == 'text':
            text = message.text
        elif content_type in ['photo', 'video', 'document']:
            text = message.caption

        if text:
            date = datetime.fromtimestamp(message.forward_date).date()

            code, response, hashtag = check.check_message(text, db.TRACKED_HASHTAGS, content_type, username)
            if code == 0:
                bot.reply_to(message, response)
            elif code == 1:
                if not db.update_stats(user_id, username, name, date, hashtag):
                    response = 'Похвально! Но отметка за сегодня уже была 😊'
                bot.reply_to(message, response)
        else:
            bot.reply_to(message, "Пересланное сообщение не содержит текста или подписи.")
    else:
        bot.reply_to(message, "Сообщение не является пересланным.")

# Запуск бота
if __name__ == '__main__':
    bot.polling(non_stop=True)
