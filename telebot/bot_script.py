import telebot
from telebot import types
import xlrd
import openpyxl
from openpyxl import Workbook
import xlwt

bot = telebot.TeleBot('6357606279:AAEaBcRmp53T6xJEDAsMyYDAgQMcwBvzDug')
ALAN_CHAT_ID = 802741951
pokupki = ''

@bot.message_handler(commands=['start'])
def start(message):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn = types.InlineKeyboardButton(text='Фрукты', callback_data='btn1')
    btn1 = types.InlineKeyboardButton(text='Сладкое', callback_data='btn2')
    btn_send_msg = types.InlineKeyboardButton(text='Другое', callback_data='send_msg')
    btn_water = types.InlineKeyboardButton(text='Вода', callback_data='btn_water')
    kb.add(btn, btn1, btn_send_msg, btn_water)
    bot.send_message(message.chat.id, 'Выберите, что должен купить Алан', reply_markup=kb)

def handle_text(message):
    bot.send_message(chat_id=ALAN_CHAT_ID, text=message.text)

@bot.callback_query_handler(func=lambda callback: True)
def check_callback_data(callback):
    global pokupki
    if callback.data == 'btn1' or callback.data == 'btn2':
        if callback.data == 'btn1':
            btn_text1, btn_text2 = 'Бананы', 'Яблоки'
            btn_data1, btn_data2 = 'btn3', 'btn4'
            btn_text3, btn_data3 = None, None
        else:
            btn_text1, btn_text2, btn_text3 = 'Торт', 'Пирог', 'Печенье'
            btn_data1, btn_data2, btn_data3 = 'btn5', 'btn6', 'btn7'
        kb = types.InlineKeyboardMarkup(row_width=1)
        btn_1 = types.InlineKeyboardButton(text=btn_text1, callback_data=btn_data1)
        btn_2 = types.InlineKeyboardButton(text=btn_text2, callback_data=btn_data2)
        kb.add(btn_1, btn_2)
        if btn_text3 and btn_data3:
            btn_3 = types.InlineKeyboardButton(text=btn_text3, callback_data=btn_data3)
            kb.add(btn_3)
        btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        kb.add(btn_back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Что именно?', reply_markup=kb)
    elif callback.data in ['btn3', 'btn4', 'btn5', 'btn6', 'btn7']:
        pokupki += {'btn3': 'Бананы', 'btn4': 'Яблоки', 'btn5': 'Торт', 'btn6': 'Пирог', 'btn7': 'Печенье'}[callback.data]
        bot.send_message(chat_id=ALAN_CHAT_ID, text=pokupki)
        bot.answer_callback_query(callback.id)
    elif callback.data == 'back':
        kb = types.InlineKeyboardMarkup(row_width=1)
        btn = types.InlineKeyboardButton(text='Фрукты', callback_data='btn1')
        btn1 = types.InlineKeyboardButton(text='Сладкое', callback_data='btn2')
        btn_send_msg = types.InlineKeyboardButton(text='Другое', callback_data='send_msg')
        btn_water = types.InlineKeyboardButton(text='Вода', callback_data='btn_water')
        kb.add(btn, btn1, btn_send_msg, btn_water)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Выберите, что должен купить Алан', reply_markup=kb)
        bot.answer_callback_query(callback.id)
    elif callback.data == 'send_msg':
        msg = bot.send_message(chat_id=callback.message.chat.id, text="Введите текст для Алана", reply_markup=types.ForceReply())
        bot.register_next_step_handler(msg, handle_text)
    elif callback.data == 'btn_water':
        kb = types.InlineKeyboardMarkup(row_width=1)
        btn_kefir = types.InlineKeyboardButton(text='Кефир', callback_data='btn_kefir')
        btn_cola = types.InlineKeyboardButton(text='Кола', callback_data='btn_cola')
        btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        kb.add(btn_kefir, btn_cola, btn_back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Выберите напиток', reply_markup=kb)
        bot.answer_callback_query(callback.id)
    elif callback.data in ['btn_kefir', 'btn_cola']:
        pokupki += {'btn_kefir': 'Кефир', 'btn_cola': 'Кола'}[callback.data]
        bot.send_message(chat_id=ALAN_CHAT_ID, text=pokupki)
        bot.answer_callback_query(callback.id)

user_text = ''

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    if message.text == "Цена покупки":
        global user_text
        bot.send_message(message.chat.id, "Введите ваш текст", reply_markup=get_keyboard())
        bot.register_next_step_handler(message, handle_next_step)

def handle_next_step(msg):
    global user_text
    user_text = msg.text
    bot.send_message(msg.chat.id, f"Вы написали: {user_text}")
    process_purchase_price(msg, user_text)

def process_purchase_price(message, user_text):
    try:
        user_text = int(user_text)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число.")
        return
    import gspread
    from google.oauth2.service_account import Credentials

    gc = gspread.service_account(filename='ace-lotus-392112-0c266134a7e1.json')
    sh = gc.open("покупкиИюль")
    worksheet = sh.worksheet("Лист1")

    cell_value = worksheet.cell(1, 1).value
    try:
        cell = int(cell_value)
    except ValueError:
        cell = 0

    znach = user_text + cell
    worksheet.update_cell(1, 1, znach)
    bot.send_message(message.chat.id, f"Обновленная цена: {znach}")

def get_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Цена покупки")
    keyboard.add(button)
    return keyboard

bot.delete_webhook()
bot.polling()
