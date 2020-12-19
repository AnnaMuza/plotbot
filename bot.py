# -*- coding: utf-8 -*-

import telebot
from PIL import Image
from telebot.apihelper import ApiException
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from wolfram import selenium, change_theme_out, change_grid_out, add_bd, get_theme, get_grid

with open('themes.png', 'rb') as f:
    themes_img = f.read()

def inline_keyboard_theme():
    keyboard = InlineKeyboardMarkup(row_width=4)
    buttons = []
    for i in range(1, 13):
        i = str(i)
        if i == get_theme():      
            buttons.append(InlineKeyboardButton(i+'  ✅', callback_data=i))
        else:
            buttons.append(InlineKeyboardButton(i, callback_data=i))
    keyboard.add(*buttons)
    return keyboard

def inline_keyboard_grid():
    keyboard = InlineKeyboardMarkup(row_width=2)
    if get_grid():
        buttons = [InlineKeyboardButton("Включить"+'  ✅', callback_data='on'), InlineKeyboardButton("Выключить", callback_data='off')]
    else:
        buttons = [InlineKeyboardButton("Включить", callback_data='on'), InlineKeyboardButton("Выключить"+'  ✅', callback_data='off')]
    keyboard.add(*buttons)
    return keyboard

#TELEBOT
bot = telebot.TeleBot('1329974992:AAEAwEdkijxhzVQfDV2v5V8Zf-jbXDE8i3E')

@bot.message_handler(commands=['start'])
def send_start(message):
    
    bot.send_message(message.chat.id, '''Напишите боту слово plot (polar plot для полярной системы координат) и любую функцию чтобы он отправил вам её график.
Например: plot x^2, plot sin(x), plot sin(x)*sin(y), polar plot r=1+sin(theta)\n
Используйте /theme для изменения цветовой гаммы графиков,
/grid для включения/отключения сетки на графиках,
/help для просмотра синтаксиса и параметров ввода''')
    send_help(message)
    add_bd(message.chat)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, '''❗ Бот использует язык Wolfram Alpha, можете применять его если работали с этим сервисом ранее ❗\n
Поддерживаемые функции: sin, cos, tan, cot, asin, acos, atan, acot, sinh, cosh, tanh, coth, sec, csc; \
exp, ln, log<основание> (пример: log10, log2), |x| или abs(x), integral(<функция>), derivative(<функция>)\n
Ипользуйте polar plot <r(theta)> для построение графика в полярной системе координат, например: polar plot r = 1 + cos(theta)\n
Для построение графика на заданном интервале используйте конструкцию "from to", например: plot sin(x) from 0 to 10\n
Для единоразового наненсения сетки на график напишите "grid" в конце функции, например: plot x^2+5 grid, plot x^3-7 from -4 to 4 grid\n
Бот также может строить несколько графиков вместе, для этого просто напишите их через запятую, например: plot x^2, x+4''')

@bot.message_handler(content_types=['text'], func=lambda x: any((x.text.lower().startswith('plot '), x.text.lower().startswith('polar plot '))) if type(x.text) == str else False)
def send_plot(message):
    bot.send_message(message.chat.id, 'График строится, подождите...')
    try:
        img = selenium(message)
        if img[0]:
            bot.send_photo(message.chat.id, img[1].content, reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id, img[1], reply_to_message_id=message.message_id)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то пошло не так, попробуйте еще раз', reply_to_message_id=message.message_id)

@bot.message_handler(commands=['theme'])
def change_theme(message):
    bot.send_photo(message.chat.id, themes_img)
    bot.send_message(message.chat.id, "Выберите подходящую тему (работает некорректно при построении графиков на заданом интервале или в пространстве):", reply_markup=inline_keyboard_theme())
    @bot.callback_query_handler(func=lambda x: x.data in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'))
    def change_theme1(call):
        try:
            change_theme_out(call)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,\
            text="Выберите подходящую тему (работает некорректно при построении графиков на заданом интервале или в пространстве):", reply_markup=inline_keyboard_theme())
        except ApiException:
            pass
        finally:
            bot.answer_callback_query(callback_query_id=call.id, text='Тема изменена на {}-ую!'.format(call.data))

@bot.message_handler(commands=['grid'])
def change_grid(message):
    bot.send_message(message.chat.id, "Включить или выключить сетку?", reply_markup=inline_keyboard_grid())
    @bot.callback_query_handler(func=lambda x: x.data in ('on', 'off'))
    def change_grid1(call):
        a = change_grid_out(call)
        try:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Включить или выключить сетку?", reply_markup=inline_keyboard_grid())
        except ApiException:
            pass
        finally:
            bot.answer_callback_query(callback_query_id=call.id, text=a)

if __name__ == "__main__":
    try:
        bot.polling()
    except ApiException:
        pass