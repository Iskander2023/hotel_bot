from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def counts_hotels():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_1 = types.KeyboardButton("1")
    button_2 = types.KeyboardButton("2")
    button_3 = types.KeyboardButton("3")
    button_4 = types.KeyboardButton("4")
    button_5 = types.KeyboardButton("5")
    markup.add(button_1, button_2, button_3, button_4, button_5)
    return markup

def count_photos():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_1 = types.KeyboardButton("1")
    button_2 = types.KeyboardButton("2")
    button_3 = types.KeyboardButton("3")
    button_4 = types.KeyboardButton("4")
    markup.add(button_1, button_2, button_3, button_4)
    return markup

def commands_button():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_1 = types.KeyboardButton("/lowprice")
    button_2 = types.KeyboardButton("/highprice")
    button_3 = types.KeyboardButton("/bestdeal")
    button_4 = types.KeyboardButton("/history")
    button_5 = types.KeyboardButton("/help")
    markup.add(button_1, button_2, button_3, button_4, button_5)
    return markup

def answer():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_1 = types.KeyboardButton("Yes")
    button_2 = types.KeyboardButton("No")
    markup.add(button_1, button_2)
    return markup