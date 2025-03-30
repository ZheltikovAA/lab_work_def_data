import sqlite3
import PySimpleGUI as sg
import password as ps
import json

def checkLimitationsOnPassword(password):
    if len(set(password)) == len(password):
        return 1
    return 0


def changePassword(password, username):
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()

    if getRestrictions(username)[0][0] == True and not checkLimitationsOnPassword(password):
        return 500

    # Обновляем пароль пользователя
    password, gamma = ps.encrypt_password(password, 3)
    cursor.execute(
        """
        UPDATE users
        SET Password = ?,Gamma = ?
        WHERE Login = ?
    """,
        (password, json.dumps(gamma), username),
    )

    # Проверяем, был ли пользователь с таким именем в базе
    if cursor.rowcount == 0:
        sg.popup(f"Error 404")
        conn.commit()
        conn.close()
        return 404
    else:
        sg.popup("Пароль обновлен.")
        conn.commit()
        conn.close()
        return 200


def blockUser(username):
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    param = getBlock(username)[0][0]
    if param == 1:
        param = 0
    else:
        param = 1

    # Обновляем пароль пользователя
    cursor.execute(
        """
        UPDATE users
        SET Blocked = ?
        WHERE Login = ?
    """,
        (param, username),
    )

    # Проверяем, был ли пользователь с таким именем в базе
    if cursor.rowcount == 0:
        sg.popup(f"Error 404")
        conn.commit()
        conn.close()
        return 404
    else:
        sg.popup("Успешно")
        conn.commit()
        conn.close()


def setLimitations(username):
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    param = getRestrictions(username)[0][0]
    if param == 1:
        param = 0
    else:
        param = 1

    # Обновляем пароль пользователя
    cursor.execute(
        """
        UPDATE users
        SET Restrictions = ?
        WHERE Login = ?
    """,
        (param, username),
    )

    # Проверяем, был ли пользователь с таким именем в базе
    if cursor.rowcount == 0:
        sg.popup(f"Error 404")
        conn.commit()
        conn.close()
        return 404
    else:
        sg.popup("Успешно")
        conn.commit()
        conn.close()


def addNewUser(user):

    if len(getUser(user)) != 0 and user != "None":
        return 0
    else:
        conn = sqlite3.connect("example.db")
        c = conn.cursor()

        # Добавление пользователя без пароля и ограничений
        c.execute(
            f"""INSERT INTO users (Login, Password)
                        VALUES ('{user}', NULL)"""
        )

        conn.commit()
        conn.close()
        return 1


def getBlock(login):
    """Функция для получения данных из базы данных"""
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()

    cursor.execute(f'SELECT Blocked FROM users WHERE Login like "{login}"')
    rows = cursor.fetchall()

    conn.close()
    return rows


def getRestrictions(login):
    """Функция для получения данных из базы данных"""
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()

    cursor.execute(f'SELECT Restrictions FROM users WHERE Login like "{login}"')
    rows = cursor.fetchall()

    conn.close()
    return rows


def getUser(login):
    """Функция для получения данных из базы данных"""
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()

    cursor.execute(f'SELECT Login FROM users WHERE Login like "{login}"')
    rows = cursor.fetchall()

    conn.close()
    return rows


def getPassword(login):
    """Функция для получения данных из базы данных"""
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()

    cursor.execute(f'SELECT Password, Gamma FROM users WHERE Login like "{login}"')
    rows = cursor.fetchall()
    print("[0][0] ", rows[0][0])
    print("[0][1] ", rows[0][1])
    conn.close()

    if rows[0][0] is None:
        return rows[0][0]
    else:
        return ps.decrypt_password(rows[0][0],3, json.loads(rows[0][1]))

def getInfoAboutUsers():
    """Функция для получения данных из базы данных"""
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()

    cursor.execute("SELECT Login, Password, Restrictions, Blocked FROM users")
    rows = cursor.fetchall()

    conn.close()
    return rows


def compareInput(login, password):
    """
    6 - установлено ограничение
    5 - пользоваьель заблокирован \n
    4 - пароль пустой \n
    2 - Успешный вход \n
    1 - Неверный пароль \n
    0 - Неверный логин \n
    """
    try:
        # Подключение к базе данных
        conn = sqlite3.connect("example.db")
        cursor = conn.cursor()
        # Проверка, что пароль не пустой
        if str(getPassword(login)) == "None":
            return 4  # Возвращаем 4, если пароль пустой

        if getBlock(login)[0][0] == True:
            return 5

        if (
            getRestrictions(login)[0][0] == True
            and checkLimitationsOnPassword(password) == 0
        ):
            return 6

        # Выполнение SQL-запроса для получения пароля пользователя
        cursor.execute("SELECT Password FROM users WHERE Login = ?", (login,))
        stored_password = cursor.fetchone()
        cursor.execute("SELECT Gamma FROM users WHERE Login = ?", (login,))
        gamma = cursor.fetchone()

        # Проверка, найдена ли запись
        if stored_password:
            stored_password = stored_password[0]

            # Сравнение введенного пароля с хранимым
            if password == ps.decrypt_password(stored_password, 3, json.loads(gamma[0])):
                return 2  # Успешный вход
            else:
                return 1  # Неверный пароль
        else:
            return 0  # Неверный логин

    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
        return 404

    finally:
        # Закрытие соединения с базой данных
        if conn:
            conn.close()
