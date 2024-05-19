import telebot
import sqlite3
from telebot import types
def read_token_from_file():
    with open('token', 'r') as file:
        # Чтение одной строки из файла
        return file.readline()

bot = telebot.TeleBot(read_token_from_file())
name = None
@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit() # синхронизирует все изменения
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегистрируем. Введите своё имя')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите свой пароль')
    bot.register_next_step_handler(message, user_pass)
def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO users (name, pass) VALUES ("%s", "%s")'% (name,password))
    conn.commit()  # синхронизирует все изменения
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Новый пользователь создан', reply_markup=markup)
    # bot.register_next_step_handler(message, user_pass)
@bot.callback_query_handler(func=lambda call:True)
def callback (call):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute(
        'SELECT * FROM users')
    # conn.commit()  # синхронизирует все изменения, здесь она не нужна
    users = cur.fetchall()
    info = ''
    for user in users:
        info += f'Имя: {user[1]} Пароль: {user[2]}\n'
    cur.close()
    conn.close()
    bot.send_message(call.message.chat.id, info)
bot.polling(non_stop=True)