from bot_calendars.bot_calendar import *
import re
from states_class.user_states import *
from loader import bot

@bot.message_handler(state=User.pricing)
def get_price_range(message: Message) -> None:
    """
    Функция проверяющая введеный пользователем диапазон цен и запрашивающая у пользователя
    диапазон расстояния на котором должен находится отель от центра города.

    :param message:
    :return:
    """
    price_range = re.sub(r"\s+", "", message.text, flags=re.UNICODE).split("-")
    if len(price_range) == 2 and price_range[0].isdigit() and price_range[1].isdigit():
            if int(price_range[0]) < int(price_range[1]):
                min_p = int(price_range[0])
                max_p = int(price_range[1])
            else:
                min_p = int(price_range[1])
                max_p = int(price_range[0])
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['min_price'] = min_p
                data['max_price'] = max_p

            bot.send_message(message.chat.id, "Введите пожалуйста диапазон расстояния,\n"
                                              "на котором отель находится от центра?(в милях, например 1 - 100)")
            bot.set_state(message.from_user.id, User.distance, message.chat.id)
    else:
        bot.send_message(message.chat.id, "Неправильный формат ввода. Попробуйте еще раз.")

@bot.message_handler(state=User.distance)
def get_distance_from_center(message: Message) -> None:
    """
    Функция проверяющая, правильно ли пользователь ввел диапазон расстояния,
    на котором находится отель от центра города.
    При корректном вооде дает пользователю возможность ввода дат заезда и выезда.
    :param message:
    :return:
    """
    city_range = re.sub(r"\s+", "", message.text, flags=re.UNICODE).split("-")
    if len(city_range) == 2 and city_range[0].isdigit() and city_range[1].isdigit():
            if int(city_range[0]) < int(city_range[1]):
                min_range = int(city_range[0])
                max_range = int(city_range[1])
            else:
                min_range = int(city_range[1])
                max_range = int(city_range[0])
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['min_range'] = min_range
                data['max_range'] = max_range
            get_check_in(message)
    else:
        bot.send_message(message.chat.id, "Неправильный формат ввода. Попробуйте еще раз")


