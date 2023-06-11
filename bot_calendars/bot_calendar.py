import telebot
from telegram_bot_calendar import DetailedTelegramCalendar
from datetime import timedelta, date
from loader import bot
from telebot.types import CallbackQuery, Message
from loguru import logger
from states_class.user_states import *
from API_info.to_work_with_API import ALL_STEPS
from handlers.custom_heandlers.info_output_state import output_info

@bot.message_handler(state=User.check_in)
def get_check_in(message):
    """
    Функция для выбора даты заезда в отель.
    Представлена ввиде календаря.
    :param message:
    :return:
    """

    calendar, step = DetailedTelegramCalendar(calendar_id=1,
                                                  current_date=date.today(),
                                                  min_date=date.today(),
                                                  max_date=date.today() + timedelta(days=365),
                                                  locale="en").build()
    bot.set_state(message.chat.id, User.calendar_1, message.chat.id)
    bot.send_message(message.chat.id, f"Укажите {ALL_STEPS[step]} заезда", reply_markup=calendar)


@logger.catch
@bot.callback_query_handler(func=None, state=User.calendar_1)
def select_check_in(call: CallbackQuery):
    """
    Функция проверяющая ввел ли пользователь дату заезда в отель.
    Если дата заезда введена, отсылает пользователю календарь для выбора даты выезда.
    :param call: CallbackQuery
    :return:
    """

    result, keyboard, step = DetailedTelegramCalendar(calendar_id=1,
                                                      current_date=date.today(),
                                                      min_date=date.today(),
                                                      max_date=date.today() + timedelta(days=365),
                                                      locale="en").process(call_data=call.data)

    if not result and keyboard:
        bot.edit_message_text(f'Укажите {ALL_STEPS[step]} заезда',
                                  call.message.chat.id,
                                  call.message.message_id,
                                  reply_markup=keyboard)

    elif result:

        with bot.retrieve_data(call.message.chat.id) as data:
            data['check_in'] = result

        bot.edit_message_text(f"Дата заезда {data['check_in']}", call.message.chat.id,
                                  call.message.message_id)

        calendar, step = DetailedTelegramCalendar(calendar_id=2,
                                                  min_date=data['check_in'] + timedelta(days=1),
                                                  max_date=data['check_in'] + timedelta(days=365),
                                                  locale="en").build()

        bot.send_message(call.message.chat.id, f'Укажите {ALL_STEPS[step]} выезда', reply_markup=calendar)
        bot.set_state(call.message.chat.id, User.calendar_2)


@logger.catch
@bot.callback_query_handler(func=None, state=User.calendar_2)
def select_check_out(call: CallbackQuery):
    """
    Функция проверяющая ввел ли пользователь дату выезда из отеля.
    Если дата введена правильно, запускается функция собирающая и выводящая информацию об отелях.
    :param call: CallbackQuery
    :return:
    """
    with bot.retrieve_data(call.message.chat.id) as data:
        result, keyboard, step = DetailedTelegramCalendar(calendar_id=2,
                                                      min_date=data['check_in'] + timedelta(days=1),
                                                      max_date=data['check_in'] + timedelta(days=365),
                                                      locale="en").process(call.data)

    if not result and keyboard:
        bot.edit_message_text(f'Укажите {ALL_STEPS[step]} выезда',
                                  call.message.chat.id,
                                  call.message.message_id,
                                  reply_markup=keyboard)

    elif result:
        with bot.retrieve_data(call.message.chat.id) as data:
            data['check_out'] = result
        bot.send_message(call.message.chat.id, f"Дата выезда {data['check_out']}")
        bot.send_message(call.message.chat.id, "Пожалуйста ожидайте, ищу отели")
        output_info(call)




























































