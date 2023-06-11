from loader import bot
from telebot.types import Message
from states_class.user_states import *
from telebot.custom_filters import StateFilter


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    bot.set_state(message.from_user.id, User.user_id, message.chat.id)
    bot.send_message(message.from_user.id,
                 '/lowprice -  вывод самых дешёвых отелей в городе\n'
                 '/highprice - вывод самых дорогих отелей в городе\n'
                 '/bestdeal -  вывод отелей, наиболее подходящих по цене и расположению от центра\n'
                 '/history - вывод истории поиска отелей')