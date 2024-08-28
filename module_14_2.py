# module_14_2.py

# Домашнее задание по теме "Выбор элементов и функции в SQL запросах".

# Задача "Средний баланс пользователя".

import sqlite3

# Для решения этой задачи вам понадобится решение предыдущей.
conn = sqlite3.connect('not_telegram.db')
cursor = conn.cursor()

# Для решения необходимо дополнить существующий код:
# 1. Удалите из базы данных not_telegram.db запись с id = 6.
cursor.execute("DELETE FROM Users WHERE id = 6")
conn.commit()

# 2. Подсчитать общее количество записей.
cursor.execute("SELECT COUNT(*) FROM Users")
total_users = cursor.fetchone()[0]
# print(f"total_users = {total_users}")

# 3. Посчитать сумму всех балансов.
cursor.execute("SELECT SUM(balance) FROM Users")
all_balances = cursor.fetchone()[0]
# print(f"all_balances = {all_balances}")

# 4. Вывести в консоль средний баланс всех пользователя.
# average_balance = all_balances / total_users if total_users > 0 else 0
# print(f"average_balance = {all_balances} / {total_users} = {average_balance}")

cursor.execute("SELECT AVG(balance) FROM Users")
average_balance = cursor.fetchone()[0]
print(average_balance)

conn.close()

# Вывод на консоль:
# 700.0
