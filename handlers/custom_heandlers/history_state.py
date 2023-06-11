import sqlite3
from states_class.user_class import *
from loader import bot


def create_db():
    """
    Функция, создающая базу данных.
    :param :
    :return: None
    """
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users_list (
            users_id INTEGER , 
            commands TEXT ,
            time_requests TEXT , 
            hotels_info TEXT 
            )    
        """)
        conn.commit()

def add_user_history(users_id: str, commands: str, time_requests: str, hotels_info: str) -> None:
    """
    Функция, добавляющая информацию о пользователе в таблицу базы данных.
    :param message:
    :return: None
    """
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO users_list(users_id, commands, time_requests, hotels_info) VALUES (?, ?, ?, ?)',
                (users_id, commands, time_requests, hotels_info))
    conn.commit()

def add_separator(string: str) -> str:
    """
    Функция разделяющая названия отелей литералом
    :param string:
    :return: string
    """
    return string.replace(';', '\n')



def show_history(message):
    """
    Функция отправляющая пользователю историю запросов отелей.
    :param message:
    :return: None
    """
    user = Users.get_user(message.from_user.id)
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        select_query = """SELECT * FROM users_list WHERE users_id = ?"""
        cur.execute(select_query, (user.u_id,))
        records = cur.fetchall()
        for row in records:
            history_to_show = f"Команда: {row[1]}\n" \
                                      f"Дата и время обращения: {row[2]}\n" \
                                      f"Список найденных отелей:\n{add_separator(row[3])}"
            bot.send_message(user.u_id, history_to_show)








