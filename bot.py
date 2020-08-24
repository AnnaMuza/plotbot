# -*- coding: utf-8 -*-

import telebot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from wolfram import selenium, string_request, change_theme_out, change_grid_out

with open('themes.png', 'rb') as f:
    themes_img = f.read()

def add_id(_id):
    with open('users_id.txt', 'r') as f:
        users_id = f.readlines()
    if not _id+'\n' in users_id:
        with open('users_id.txt', 'a') as f:
            f.write(_id+'\n')


#TELEBOT
bot = telebot.TeleBot('1329974992:AAEAwEdkijxhzVQfDV2v5V8Zf-jbXDE8i3E')

@bot.message_handler(commands=['start'])
def send_start(message):
    bot.send_message(message.chat.id, '''Напишите боту слово plot и любую функцию чтобы он отправил вам её график.
Например: plot x^2, plot sin(x), plot sin(x)*sin(y).\n
Используйте /theme для изменения цветовой гаммы графиков,
/grid для включения/отключения сетки на графиках,
/help для просмотра синтаксиса и параметров ввода.''')
    send_help(message)
    add_id(str(message.chat.id))

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, '''Поддерживаемые функции: sin, cos, tan, cot, asin, acos, atan, acot, sinh, cosh, tanh, coth, sec, csc; \
exp, ln, log<основание> (пример: log10, log2), |x| или abs(x), integral(<функция>), derivative(<функция>).\n
Для построение графика на заданном интервале используйте конструкцию "from to", например: plot sin(x) from 0 to 10.\n
Для единоразового наненсения сетки на график напишите "grid" в конце функции, например: plot x^2+5 grid, plot x^3-7 from -4 to 4 grid.''')

@bot.message_handler(commands=['theme'])
def change_theme(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('1 (default)', '2', '3', '4')
    keyboard.row('5', '6', '7', '8')
    keyboard.row('9', '10', '11', '12')
    bot.send_message(message.chat.id, "Выберите подходящую тему (работает некорректно при построении графиков на заданом интервале или в пространстве):", reply_markup=keyboard)
    keyboard = ReplyKeyboardRemove()
    bot.send_photo(message.chat.id, themes_img)
    @bot.message_handler(func=lambda x: x.text in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'], content_types=['text'])
    def change_theme1(message):
        change_theme_out(message)
        bot.send_message(message.chat.id, "Тема изменена!", reply_markup=keyboard)

@bot.message_handler(func=lambda x: x.text.lower().startswith('plot '), content_types=['text'])
def send_plot(message):
    bot.send_message(message.chat.id, 'График строится, подождите...')
    try:
        img = selenium(message)
        if img[0]:
            bot.send_photo(message.chat.id, img[1].content)
        else:
            bot.send_message(message.chat.id, img[1])
    except Exception:
        bot.send_message(message.chat.id, 'Что-то пошло не так, попробуйте еще раз')

@bot.message_handler(commands=['grid'])
def change_grid(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Включить', 'Выключить')
    bot.send_message(message.chat.id, "Включить или выключить сетку?", reply_markup=keyboard)
    keyboard = ReplyKeyboardRemove()
    @bot.message_handler(func=lambda x: x.text in ['Включить', 'Выключить'], content_types=['text'])
    def change_grid1(message):
        a = change_grid_out(message)
        bot.send_message(message.chat.id, a, reply_markup=keyboard)
    
bot.polling()