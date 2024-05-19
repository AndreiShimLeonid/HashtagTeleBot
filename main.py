import telebot
from telebot import types
def read_token_from_file():
    with open('token', 'r') as file:
        # Чтение одной строки из файла
        return file.readline()

bot = telebot.TeleBot(read_token_from_file())

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Погладить бота')
    btn2 = types.KeyboardButton('Наругать бота')
    btn3 = types.KeyboardButton('Спросить про статистику')
    markup.row(btn1)
    markup.row(btn2, btn3)
    file = open('cordon.jpg', 'rb')
    bot.send_photo(message.chat.id, file)
    bot.send_message(message.chat.id, f'Приветствую тебя, {message.from_user.first_name}!', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)
    # bot.send_message(message.chat.id, message)
def on_click(message):
    if message.text == 'Погладить бота':
        bot.send_message(message.chat.id, f'Мурр-мяу!')
    elif message.text =='Наругать бота':
        bot.send_message(message.chat.id, f'Виноват! Исправлюсь!')
    elif message.text =='Спросить про статистику':
        bot.send_message(message.chat.id, f'Статистика... Пока не готова, подождите некоторе время.')

@bot.message_handler(content_types=['photo'])
def image_process(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Посмотреть другие картинки', url='https://yandex.ru/images?')
    btn2 = types.InlineKeyboardButton('Удалить картинку', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Изменить сообщение', callback_data='edit')
    markup.row(btn1)
    markup.row(btn2,btn3)
    bot.reply_to(message, f'That is awesome!, {message.from_user.first_name}', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback:True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id-1)
    elif callback.data == 'edit':
        bot.edit_message_text('edit text', callback.message.chat.id, callback.message.message_id)

# Обработка текста сообщения пользователя
@bot.message_handler()
def info(message):
    if 'как дела' in message.text.lower():
        bot.send_message(message.chat.id, "хорошо, а у тебя?")
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')
    # elif message.text.lower() == 'stats':
    #     stats(message)

# bot.infinity_polling()
bot.polling(non_stop=True)