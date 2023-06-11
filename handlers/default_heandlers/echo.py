from telebot.types import Message

from loader import bot


#Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    bot.reply_to(message, "Пожалуйста выберите корректную команду.")
    bot.delete_message(message.chat.id, message.message_id)
