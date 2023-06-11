from loader import bot
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from loguru import logger
from handlers.custom_heandlers.history_state import create_db

if __name__ == '__main__':
    create_db()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
    logger.add("debug.log", format="{time} {level} {message}",
               level="DEBUG", rotation="100 MB", compression="zip")
    logger.debug("Error")
    logger.info('Information message')
    logger.warning('Warning')