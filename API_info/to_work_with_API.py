import requests
import re
from datetime import datetime
from config_data import config

ALL_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'}

url_for_destination_id = "https://hotels4.p.rapidapi.com/locations/v2/search"

url_properties_list = "https://hotels4.p.rapidapi.com/properties/list"

url_get_photos_hotels = url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

headers = {
            "X-RapidAPI-Key": config.RAPID_API_KEY,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}

def delete_html_simbols(data: str) -> str:
    """
    Функция, удаляющая спецсимволы HTML.
    :param data: строка, содержащая теги HTML
    :return: строка без HTML тегов
    """
    result = re.compile(r'<.*?>')
    return result.sub('', data)


def request_to_api(url: str, headers: dict, querystring: dict) -> dict or None:
    """
    Функция, производящая запрос к API.
    :param url: ссылка
    :param headers: headers
    :param querystring: parameters
    :return:
    """

    try:
        responses = requests.request("GET", url,
                                    headers=headers,
                                    params=querystring,
                                    timeout=10)
        if responses.status_code == requests.codes.ok:
            return responses.text
    except requests.exceptions.Timeout:
        return None

def modify_symbol(num: str) -> int:
    """
    Функция для удаления запятой в  возвращаемом значении стоимости.
    :param num: строка
    :return: число
    """
    return int(re.sub(r'[^0-9]+', "", num))

def price_for_accommodation(date_1: str, date_2: str, price_current: str) -> int:
    """
    Функция считющая стоимость проживания за все время пребывания в отеле.
    :param date_1: дата заезда
    :param date_2: дата выезда
    :param price_current: стоимость проживания за сутки
    :return: стоимость проживания в отеле
    """

    d_1 = datetime.strptime(str(date_1), "%Y-%m-%d")
    d_2 = datetime.strptime(str(date_2), "%Y-%m-%d")
    amount_of_days = int((d_2 - d_1).days)
    return int(price_current) * amount_of_days

