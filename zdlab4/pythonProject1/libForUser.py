import sqlite3
import PySimpleGUI as sg
import password as PS
import json
import cryptInfo as crypt

def checkLimitationsOnPassword(password):
    if len(set(password)) == len(password):
        return 1
    return 0

def changePassword(password, username):
    conn = sqlite3.connect(crypt.TEMP_DECRYPTED_FILE)
    cursor = conn.cursor()

    if getRestrictions(username)[0][0] == True and not checkLimitationsOnPassword(password):
        return 500
    encrypt, gamma = PS.encrypt_password(password,3)
    # Обновляем пароль пользователя
    cursor.execute("""
        UPDATE users
        SET Password = ?, Gamma = ?
        WHERE Login = ?
    """, (encrypt, json.dumps(gamma), username))

    # Проверяем, был ли пользователь с таким именем в базе
    if cursor.rowcount == 0:
        sg.popup(f'Error 404')
        conn.commit()
        conn.close()
        return 404
    else:
        sg.popup("Пароль обновлен.")
        conn.commit()
        conn.close()
        return 200

def blockUser(username):
    conn = sqlite3.connect(crypt.TEMP_DECRYPTED_FILE)
    cursor = conn.cursor()
    param = getBlock(username)[0][0]
    if param == 1: 
        param = 0
    else: 
        param = 1

    # Обновляем пароль пользователя
    cursor.execute("""
        UPDATE users
        SET Blocked = ?
        WHERE Login = ?
    """, (param, username))

    # Проверяем, был ли пользователь с таким именем в базе
    if cursor.rowcount == 0:
        sg.popup(f'Error 404')
        conn.commit()
        conn.close()
        return 404
    else:
        sg.popup("Успешно")
        conn.commit()
        conn.close()

def setLimitations(username):
    conn = sqlite3.connect(crypt.TEMP_DECRYPTED_FILE)
    cursor = conn.cursor()
    param = getRestrictions(username)[0][0]
    if param == 1: 
        param = 0
    else: 
        param = 1

    # Обновляем пароль пользователя
    cursor.execute("""
        UPDATE users
        SET Restrictions = ?
        WHERE Login = ?
    """, (param, username))

    # Проверяем, был ли пользователь с таким именем в базе
    if cursor.rowcount == 0:
        sg.popup(f'Error 404')
        conn.commit()
        conn.close()
        return 404
    else:
        sg.popup("Успешно")
        conn.commit()
        conn.close()

def addNewUser(user):

    if len(getUser(user)) != 0 and user != 'None':
        return 0
    else:
        conn = sqlite3.connect(crypt.TEMP_DECRYPTED_FILE)
        c = conn.cursor()

        # Добавление пользователя без пароля и ограничений
        c.execute(f'''INSERT INTO users (Login, Password)
                        VALUES ('{user}', NULL)''')

        conn.commit()
        conn.close()
        return 1
    
def getBlock(login):
    """Функция для получения данных из базы данных"""
    conn = sqlite3.connect(crypt.TEMP_DECRYPTED_FILE)
    cursor = conn.cursor()
    
    cursor.execute(f'SELECT Blocked FROM users WHERE Login like "{login}"')
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def getRestrictions(login):
    """Функция для получения данных из базы данных"""
    conn = sqlite3.connect(crypt.TEMP_DECRYPTED_FILE)
    cursor = conn.cursor()
    
    cursor.execute(f'SELECT Restrictions FROM users WHERE Login like "{login}"')
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def getUser(login):
    """Функция для получения данных из базы данных"""
    conn = sqlite3.connect(crypt.TEMP_DECRYPTED_FILE)
    cursor = conn.cursor()
    
    cursor.execute(f'SELECT Login FROM users WHERE Login like "{login}"')
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def getPassword(login):
    """Функция для получения данных из базы данных"""
    conn = sqlite3.connect(crypt.TEMP_DECRYPTED_FILE)
    cursor = conn.cursor()
    
    cursor.execute(f'SELECT Password FROM users WHERE Login like "{login}"')
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def getInfoAboutUsers():
    """Функция для получения данных из базы данных"""
    conn = sqlite3.connect(crypt.TEMP_DECRYPTED_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT Login, Password, Restrictions, Blocked FROM users")
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def getGammaFromDB(login):
    """Функция для получения данных гаммы из базы данных"""
    conn = sqlite3.connect(crypt.TEMP_DECRYPTED_FILE)
    cursor = conn.cursor()
    
    cursor.execute(f'SELECT Gamma FROM users WHERE Login like "{login}"')
    rows = cursor.fetchall()
    
    conn.close()
    return json.loads(rows[0][0])

def compareInput(login, password):
    """
    6 - установлено ограничение
    5 - пользователь заблокирован \n
    4 - пароль пустой \n
    2 - Успешный вход \n
    1 - Неверный пароль \n
    0 - Неверный логин \n
    """
    try:
        
        # Подключение к базе данных
        conn = sqlite3.connect(crypt.TEMP_DECRYPTED_FILE)
        
        cursor = conn.cursor()
        # Проверка, что пароль не пустой
        if str(getPassword(login)[0][0]) == 'None':
            return 4  # Возвращаем 4, если пароль пустой
        
        if getBlock(login)[0][0] == True:
            return 5
    
        if getRestrictions(login)[0][0] == True and checkLimitationsOnPassword(password) == 0:
            return 6
        
        # Выполнение SQL-запроса для получения пароля пользователя
        cursor.execute("SELECT Password FROM users WHERE Login = ?", (login,))
        stored_password = cursor.fetchone()

        # Проверка, найдена ли запись
        if stored_password:
            stored_password = stored_password[0]
            gamma = getGammaFromDB(login)
            print(gamma)
            # Сравнение введенного пароля с хранимым
            if password == PS.decrypt_password(stored_password,3,gamma):
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