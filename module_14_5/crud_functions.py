# crud_functions.py

import sqlite3


def initiate_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Таблица продуктов
    cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      description TEXT,
                      price INTEGER NOT NULL)''')

    # Дополните файл crud_functions.py, написав и дополнив в нём следующие функции:
    # initiate_db дополните созданием таблицы Users, если она ещё не создана при помощи SQL запроса.
    # Эта таблица должна содержать следующие поля:
    # id - целое число, первичный ключ
    # username - текст (не пустой)
    # email - текст (не пустой)
    # age - целое число (не пустой)
    # balance - целое число (не пустой)

    # Таблица пользователей
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT NOT NULL UNIQUE,
                      email TEXT NOT NULL,
                      age INTEGER NOT NULL,
                      balance INTEGER NOT NULL DEFAULT 1000)''')

    conn.commit()
    conn.close()


def get_all_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    conn.close()
    return products


def add_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    for i in range(1, 5):
        cursor.execute("SELECT * FROM Products WHERE title = ?", (f'Продукт {i}',))
        product = cursor.fetchone()

        if product is None:
            cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                           (f'Продукт {i}', f'Описание {i}', i * 100))

    conn.commit()
    conn.close()


# add_user(username, email, age), которая принимает: имя пользователя, почту и возраст.
# Данная функция должна добавлять в таблицу Users вашей БД запись с переданными данными.
# Баланс у новых пользователей всегда равен 1000. Для добавления записей в таблице используйте SQL запрос.
def add_user(username, email, age):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, 1000)",
                   (username, email, age))
    conn.commit()
    conn.close()


# is_included(username) принимает имя пользователя и возвращает True,
# если такой пользователь есть в таблице Users, в противном случае False.
# Для получения записей используйте SQL запрос.
def is_included(username):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None
