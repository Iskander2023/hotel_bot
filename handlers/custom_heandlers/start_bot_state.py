from keyboards.reply.reply_buttons import *
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from API_info.to_work_with_API import *
from bot_calendars.bot_calendar import *
from handlers.custom_heandlers.history_state import *
import json

@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """
    Функция - обработчик сообщений. Реагирует на команду '/start' и предлагает пользователю выбор дальнейших команд.
    :param message:
    :return:
    """
    bot.set_state(message.from_user.id, User.user_id, message.chat.id)
    bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name} пожалуйста выберите действие: ',
                                                                                    reply_markup=commands_button())

@bot.message_handler(state=User.user_id)
def get_commands(message: Message) -> None:
    """
    Функция, запускающая команды: 'lowprice', 'highprice', 'bestdeal', 'history', 'help'.
    Определяет корректность вводимых пользователем данных
    С данной функции осуществляется начало сбора информации
    по команде, для дальнейшего сохранения в базу данных.
    :param message:
    :return:
    """
    if message.text == '/lowprice' or message.text == '/highprice' or message.text == '/bestdeal':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['user_id'] = message.chat.id
            data['request_time'] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            data['commands'] = message.text
        bot.send_message(message.from_user.id, 'В каком городе ищем?')
        bot.set_state(message.from_user.id, User.city, message.chat.id)

        user = Users.get_user(message.from_user.id)
        user.commands = message.text
        user.u_id = message.chat.id
        user.request_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    elif message.text == "/history":
        bot.send_message(message.from_user.id, 'Загружаю историю поиска отелей')
        show_history(message)

    elif message.text == '/help':
        bot.send_message(message.from_user.id,
        '/lowprice -  вывод самых дешёвых отелей в городе\n' 
        '/highprice - вывод самых дорогих отелей в городе\n' 
        '/bestdeal -  вывод отелей, наиболее подходящих по цене и расположению от центра\n' 
        '/history - вывод истории поиска отелей')

    else:
        bot.send_message(message.from_user.id, ' Выберите команду из предоставленых')

@bot.message_handler(state=User.city)
def city(message: Message) -> None:
    """
    Функция для определения локации поиска. Определяет корректность вводимых пользователем данных
    и существовоание такого города в базе. Если данные введены коректно и такой город существует,
    отсылает пользователю список инлайн кнопок с названиями городов.
    :param message:
    :return:
    """
    correct_city_name = True
    for sym in message.text:
        if sym.isalpha() and len(message.text) < 25:
            continue
        else:
            if sym in [" ", "-"]:
                continue
            else:
                correct_city_name = False
                break

    if correct_city_name:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
        querystring_for_destination_id = {"query": data['city'],
                                          "locale": "en_US",
                                          "currency": "USD"
                                          }

        response = request_to_api(url=url_for_destination_id,
                                  headers=headers,
                                  querystring=querystring_for_destination_id)

        suggestions_entities = json.loads(response)

        if response and len(suggestions_entities["suggestions"][1]['entities']) > 0:
            pattern = r'(?<="CITY_GROUP",).+?[\]]'
            find = re.search(pattern, response)
            suggestions = json.loads(f"{{{find[0]}}}")
            cities = list()

            for dest_id in suggestions['entities']:
                clear_destination = delete_html_simbols(dest_id['caption'])
                cities.append({'city_name': clear_destination,
                               'destination_id': dest_id['destinationId']})
            destinations = InlineKeyboardMarkup()

            for city in cities:
                destinations.add(InlineKeyboardButton(text=city['city_name'],
                                                      callback_data=f'{"city_" + city["destination_id"]}'))
            bot.send_message(message.chat.id, "Выберите локацию", reply_markup=destinations)
            bot.set_state(message.from_user.id, User.no_locations, message.chat.id)

        else:
            bot.send_message(message.chat.id, "Пожалуйста, проверьте, правильно ли указано название города\n"
                                                                                      "и попробуйте еще раз")
    else:
        bot.send_message(message.chat.id, "Некорекктное название города\n"
                                                     "попробуйте еще раз")

    @bot.message_handler(state=User.no_locations)
    def again_city(message: Message) -> None:
        """
        Функция отправляющая пользователю список инлайн кнопок с названиями городов
        в случае, если пользователь введет что-то с клавиатуры в состоянии выбора города.
        :param message:
        :return:
        """
        bot.send_message(message.chat.id, "Выберите локацию", reply_markup=destinations)


@logger.catch
@bot.callback_query_handler(func=lambda call: call.data.startswith("city_"))
def location_processing(call: CallbackQuery) -> None:
    """
    Функция проверяющая корректность выбраного пользователем города и предоставляющая ему выбор количества отелей.
    :param call:
    :return:
    """
    with bot.retrieve_data(call.from_user.id) as data:
        data['destination_id'] = call.data[5:]

    bot.edit_message_text(chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=f"Выберите количество отелей от 1 до 5")
    bot.set_state(call.from_user.id, User.destination_id)

@bot.message_handler(state=User.destination_id)
def get_number_of_hotels(message: Message) -> None:
    """
    Функция проверяющая корректность вводимого пользователем количества отелей
    и предоставляющая ему возможность загрузки фотографий.
    :param message:
    :return:
    """
    number_hotels = message.text
    if number_hotels.isdigit() and 0 < int(number_hotels) <= 5:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['number_of_hotels'] = number_hotels
        bot.send_message(message.chat.id, 'Загрузить фотографии отелей?',
                                 reply_markup=answer())
        bot.set_state(message.from_user.id, User.number_of_hotels, message.chat.id)
    else:
        bot.send_message(message.from_user.id, 'Выберите от 1 до 5 отелей')

@bot.message_handler(state=User.number_of_hotels)
def get_photos_info(message: Message) -> None:
    """
    Функция проверяющая корректность вводимого пользователем ответа (Yes/No).
    Если пользователь хочет загрузить фотографии, функция запрашивает количество фото,
    в случае отрицательного ответа, предоставляет пользователю выбор даты заезда и выезда,
    также в случае отрицательного ответа и команды /bestdeal запрашивает у пользователя
    диапазон цен за сутки проживания в отеле.

    :param message:
    :return:
    """
    answer = message.text
    if answer == "Yes" or answer == "yes":
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photos_upload'] = True
        bot.send_message(message.from_user.id, 'Сколько фотографий загрузить? Не более 4х',
                                                                reply_markup=count_photos())
        bot.set_state(message.from_user.id, User.photos_upload, message.chat.id)

    elif answer == "No" or answer == "no":
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if data["commands"] == "/lowprice" or data['commands'] == "/highprice":
                data['photos_upload'] = False
                get_check_in(message)
            else:
                bot.send_message(message.from_user.id,
                'Введите пожалуйста диапазон цен за сутки проживания в отеле (например 1 - 5000)')
                bot.set_state(message.from_user.id, User.pricing, message.chat.id)

    else:
        bot.send_message(message.from_user.id, "Пожалуйста выберите Yes/No")

@bot.message_handler(state=User.photos_upload)
def check_count_photos(message: Message) -> None:
    """
    Функция проверяющая корректность вводимого пользователем количества фотографий.
    В случае  выбора пользователем команды /bestdeal запрашивает у пользователя
    диапазон цен за сутки проживания в отеле.
    :param message:
    :return:
    """
    count_photo = message.text
    if count_photo.isdigit():
        if int(count_photo) > 4:
            bot.send_message(message.from_user.id, 'Выберите от 1 до 4 фотографий отелей')
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data["number_of_photos"] = int(count_photo)
            if data["commands"] == "/lowprice" or data["commands"] == "/highprice":
                get_check_in(message)


            else:
                bot.send_message(message.from_user.id, 'Введите пожалуйста диапазон за сутки проживания в отеле (например 1 - 5000)')
                bot.set_state(message.from_user.id, User.pricing, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "Пожалуйста введите цифрами количество фотографий для загрузки")

