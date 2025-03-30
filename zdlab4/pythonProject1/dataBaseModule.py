import os
import sqlite3
import PySimpleGUI as sg

def create_and_check_database(db_name):
    # Создание файла базы данных
    # Проверка существования файла
    if not os.path.exists(db_name):
        return 1
    conn = sqlite3.connect(db_name)
    # Закрытие соединения
    conn.close()
    return 0

def create_scheme():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 Login TEXT PRIMARY KEY,
                 Password TEXT,
                 Restrictions BOOLEAN DEFAULT FALSE,
                 Blocked BOOLEAN DEFAULT FALSE,
                 Gamma TEXT
                 )
              ''')

    conn.commit()
    conn.close()

def insert_users():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Добавление пользователя с стандартным паролем и без ограничений
    c.execute('''INSERT INTO users (Login)
                 VALUES ('admin')''')

    # Добавление пользователя без пароля и ограничений
    # c.execute(f'''INSERT INTO users (Login, Password)
    #              VALUES ('{user}', NULL)''')

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_and_check_database('example.db')
    create_scheme()
    insert_users()
