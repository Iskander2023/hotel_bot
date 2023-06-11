from telebot.handler_backends import State, StatesGroup


class User(StatesGroup):
    user_id = State()
    commands = State()
    city = State()
    destination_id = State()
    number_of_hotels = State()
    number_of_photos = State()
    photos_upload = State()
    no_locations = State()
    calendar_1 = State()
    calendar_2 = State()
    pricing = State()
    min_price = State()
    max_price = State()
    distance = State()
    min_range = State()
    max_range = State()
    check_in = State()
    check_out = State()
    output = State()
    hotels_info_list = State()
    his = State()


