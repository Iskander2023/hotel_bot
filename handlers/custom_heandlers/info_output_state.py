from loguru import logger
from API_info.to_work_with_API import *
from handlers.custom_heandlers.history_state import *
from telebot import types
from telebot.types import CallbackQuery
import json

@logger.catch
def output_info(call: CallbackQuery) -> None:
    """
    Функция собирающая и выводящая информацию об отелях и фотографии в зависисмости от введенной команды.
    Также здесь заполняется база данных для команды /history.
    :param call:
    :return:
    """
    hotels_info = ""
    with bot.retrieve_data(call.from_user.id) as data:
        if data["commands"] == "/lowprice" or data["commands"] == "/highprice":
            querystring_properties_list = {"destinationId" : data['destination_id'],
                                       "pageNumber" : "1",
                                       "pageSize" : data["number_of_hotels"],
                                       "checkIn" : data["check_in"],
                                       "checkOut" : data["check_out"],
                                       "adults1" : "1",
                                       "sortOrder" : "PRICE_HIGHEST_FIRST" if data["commands"] == "/highprice" else "PRICE",
                                       "locale" : "en_US",
                                       "currency" : "USD"}


        else:
            querystring_properties_list = {"destinationId": data['destination_id'],
                                       "pageNumber": "1",
                                       "pageSize": data["number_of_hotels"],
                                       "checkIn": data["check_in"],
                                       "checkOut": data["check_out"],
                                       "adults1": "1",
                                       "priceMin": data["min_price"],
                                       "priceMax": data["max_price"],
                                       "sortOrder": "DISTANCE_FROM_LANDMARK",
                                       "locale": "en_US",
                                       "currency": "USD",
                                       "landmarkIds": "City center"}

        response_properties_list = request_to_api(url=url_properties_list, headers=headers, querystring=querystring_properties_list)
        if not response_properties_list:
            bot.send_message(call.message.chat.id, "Произошла ошибка. Попробуйте снова.")
        else:
            result = json.loads(response_properties_list)["data"]["body"]["searchResults"]["results"]

            if result:
                with bot.retrieve_data(call.from_user.id) as data:
                    data["hotels_info_list"] = {hotel.get('id'):
                                             {'hotel_name': hotel.get('name'),
                                              'hotel_address': hotel['address'].get('streetAddress'),
                                              'distance_to_center': hotel['landmarks'][0].get('distance'),
                                              'hotel_website': f"https://ru.hotels.com/ho{hotel.get('id')}",
                                              'price_current': modify_symbol(hotel['ratePlan']['price'].get('current')),
                                              'photos': []
                                              } for hotel in result}
                    if data["photos_upload"] is False:

                        for hotels in data["hotels_info_list"]:
                            total_price = price_for_accommodation(data["check_in"],
                                                                  data["check_out"],
                                                                  data['hotels_info_list'][hotels]['price_current'])

                            bot.send_message(call.message.chat.id,
                                             f"Отель: {data['hotels_info_list'][hotels]['hotel_name']}\n"
                                             f"Адрес: {data['hotels_info_list'][hotels]['hotel_address']}\n"
                                             f"Период проживания: с {data['check_in']} по {data['check_out']}\n"
                                             f"Сайт отеля: {data['hotels_info_list'][hotels]['hotel_website']}\n"
                                             f"Расстояние до центра: {data['hotels_info_list'][hotels]['distance_to_center']}\n"
                                             f"Стоимость проживания за одни сутки: {data['hotels_info_list'][hotels]['price_current']}$\n"
                                             f"Общая стоимость проживания: {total_price}$")


                            hotels_info += f"{data['hotels_info_list'][hotels]['hotel_name']};"

                        add_user_history(data['user_id'], data['commands'], data['request_time'], hotels_info)
                    else:
                        for h_id in data["hotels_info_list"]:

                            hotels_info += f"{data['hotels_info_list'][h_id]['hotel_name']};"

                            querystring_to_photos = {"id": h_id}
                            response_photos = request_to_api(url=url_get_photos_hotels,
                                                              headers=headers,
                                                              querystring=querystring_to_photos)

                            if not response_photos:
                                bot.send_message(call.message.chat.id, "Пожалуйста извините, чтото пошло не так")

                            else:
                                result_hotels_photos = json.loads(response_photos)["roomImages"][0]["images"][0:data["number_of_photos"]]

                                for photo in result_hotels_photos:
                                    photo_url = photo['baseUrl'].format(size="z")
                                    data["hotels_info_list"][h_id]['photos'].append(photo_url)

                                    total_price = price_for_accommodation(data["check_in"],
                                                                              data["check_out"],
                                                                              data['hotels_info_list'][h_id]['price_current'])

                                    text = f"Отель: {data['hotels_info_list'][h_id]['hotel_name']}\n" \
                                           f"Адрес: {data['hotels_info_list'][h_id]['hotel_address']}\n" \
                                           f"Период проживания: с {data['check_in']} по {data['check_out']}\n" \
                                           f"Сайт отеля: {data['hotels_info_list'][h_id]['hotel_website']}\n" \
                                           f"Расстояние до центра: {data['hotels_info_list'][h_id]['distance_to_center']}\n" \
                                           f"Стоимость проживания за одни сутки: {data['hotels_info_list'][h_id]['price_current']}$\n" \
                                           f"Общая стоимость проживания: {total_price}$"

                                    photos = [types.InputMediaPhoto(media=url, caption=text) if number == 0
                                                                      else types.InputMediaPhoto(media=url)
                                            for number, url in enumerate(data["hotels_info_list"][h_id]['photos'])]

                                bot.send_media_group(call.message.chat.id, photos)
                        add_user_history(data['user_id'], data['commands'], data['request_time'], hotels_info)
    bot.delete_state(call.from_user.id)