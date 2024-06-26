import os
import telebot
import json
from db import read_token_from_file

# Укажите ваш токен API, выданный BotFather
bot = telebot.TeleBot(read_token_from_file('token'))


# Функция для проверки, существует ли пользователь в файле
def user_exists(user_id, username):
    if not os.path.exists('user_info.txt'):
        return False
    with open('user_info.txt', 'r', encoding='utf-8') as f:
        for line in f:
            user_info = json.loads(line)
            if user_info['id'] == user_id or user_info['username'] == username:
                return True
    return False


# Функция для записи информации о пользователе в файл
def save_user_info(user):
    if user_exists(user.id, user.username):
        print(f"User with ID {user.id} or username {user.username} already exists.")
        return
    user_info = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'language_code': user.language_code,
        'is_bot': user.is_bot
    }
    with open('user_info.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(user_info, ensure_ascii=False) + '\n')
    print(f"Saved user with ID {user.id}.")


# Функция для вывода информации о пользователях из файла на консоль
def show_users_info():
    try:
        with open('user_info.txt', 'r', encoding='utf-8') as f:
            for line in f:
                user_info = json.loads(line)
                print(user_info)
    except FileNotFoundError:
        print("No user info file found.")


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Forward me a message from another user, "
                          "and I'll save their info to a file. "
                          "Use /show_users to display saved users.")


# Обработчик команды /show_users
@bot.message_handler(commands=['show_users'])
def handle_show_users(message):
    show_users_info()
    bot.reply_to(message, "User info has been printed to the console.")


# Обработчик всех сообщений
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if message.forward_from:
        original_user = message.forward_from
        save_user_info(original_user)
        bot.reply_to(message, f"Information about the original sender has been saved.")
    else:
        user = message.from_user
        save_user_info(user)
        bot.reply_to(message, "Your information has been saved.")


# Запуск бота
if __name__ == '__main__':
    bot.polling(non_stop=True)
