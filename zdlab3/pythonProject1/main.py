import PySimpleGUI as sg
import libForUser
import dataBaseModule

# from adminWindow import windowAdminCall

menu_def = [["&Файл", ["Выход"]], ["&Справка", ["&О программе..."]]]


def setNewPassword(window, login):
    layoutToChangePasswordn = [
        [sg.Text("Новый пароль:")],
        [sg.InputText("", key="NewPass", password_char="*")],
        [sg.Text("Подтвердите новый пароль:")],
        [sg.InputText("", key="RepeatNewPass", password_char="*")],
        [sg.Button("Задать пароль")],
    ]

    window3 = sg.Window("Панель смены пароля", layoutToChangePasswordn)
    while True:
        event, values = window3.read()
        match event:
            case "Задать пароль":
                newValuePass = values["NewPass"] == values["RepeatNewPass"]
                if newValuePass:
                    result = libForUser.changePassword(values["RepeatNewPass"], login)
                    match result:
                        case 200:
                            window3.close()
                            window.un_hide()
                            break
                        case 500:
                            sg.popup(
                                "На данного пользователя наложено ограничение. \n Пожалуйста уберите повторяющиеся символы"
                            )
                else:
                    sg.popup("Пароли не совпадают!")
            case "Выход":
                window3.close()
                window.un_hide()
                break
            case sg.WIN_CLOSED:
                window3.close()
                window.un_hide()
                break


def changePassword(window, login):
    layoutToChangePasswordn = [
        [sg.Text("Старый пароль:")],
        [sg.InputText("", key="OldPass", password_char="*")],
        [sg.Text("Новый пароль:")],
        [sg.InputText("", key="NewPass", password_char="*")],
        [sg.Text("Подтвердите новый пароль:")],
        [sg.InputText("", key="RepeatNewPass", password_char="*")],
        [sg.Button("Выход"), sg.Button("Сменить пароль")],
    ]

    window3 = sg.Window("Панель смены пароля", layoutToChangePasswordn)
    while True:
        event, values = window3.read()
        match (event):
            case "Сменить пароль":
                newValuePass = values["NewPass"] == values["RepeatNewPass"]
                if values["NewPass"] == values["OldPass"]:
                    sg.popup("Старый и Новый пароли совпадают!")
                elif (
                    newValuePass
                    and values["OldPass"] == libForUser.getPassword(login)
                ):
                    result = libForUser.changePassword(values["RepeatNewPass"], login)
                    match (result):
                        case 200:
                            window3.close()
                            window.un_hide()
                            break
                        case 500:
                            sg.popup(
                                "На данного пользователя наложено ограничение. \n Пожалуйста уберите повторяющиеся символы"
                            )
                else:
                    sg.popup("Пароли не совпадают!")
            case "Выход":
                window3.close()
                window.un_hide()
                break
            case sg.WIN_CLOSED:
                window3.close()
                window.un_hide()
                break


def windowUserCall(window, login):
    layoutToAdmin = [
        [sg.Menu(menu_def)],
        [sg.Button("Выход из учетной записи"), sg.Button("Сменить пароль")],
    ]

    window3 = sg.Window("Пользовательская панель", layoutToAdmin)
    while True:
        event, values = window3.read()
        match (event):
            case "О программе...":
                sg.popup(
                    "Выполнила: \n Самсонова Мария Дмитриевна \n Группа А-05-21 \n Вариант 19"
                )
            case "Сменить пароль":
                window3.hide()
                changePassword(window3, login)

            case "Выход из учетной записи":
                window3.close()
                window.un_hide()
                break

            case sg.WIN_CLOSED:
                window3.close()
                window.un_hide()
                break


def windowAdminCall(window, rows, login):
    columns = ["Логин", "Пароль", "Ограничения", "Блокировка"]
    layoutToAdmin = [
        [sg.Menu(menu_def)],
        [
            sg.Button("Выход из учетной записи"),
            sg.Button("Сменить пароль"),
            sg.Button("Добавить пользователя"),
        ],
        [
            sg.Table(
                values=rows,
                headings=columns,
                max_col_width=100,
                auto_size_columns=True,
                display_row_numbers=False,
                justification="center",
                enable_events=True,
                alternating_row_color="light blue",
                key="TABLE",
            )
        ],
        [sg.Text("Выбранный пользователь"), sg.Text("", size=(40, 1), key="OUTPUT")],
        [
            sg.Checkbox("Блокировка учетной записи", key="block", enable_events=True),
            sg.Checkbox("Ограничение пароля", key="limitation", enable_events=True),
        ],
    ]

    window2 = sg.Window("Административная панель", layoutToAdmin)
    while True:
        event, values = window2.read()

        match (event):
            case "Добавить пользователя":
                result = sg.popup_get_text(
                    "Введите новое имя пользователя", title="Новое имя пользователя"
                )

                foo = libForUser.addNewUser(result)
                if foo == 0:
                    sg.popup(f"Пользователь {result} существует")
                else:
                    sg.popup(f"Пользователь {result} был добавлен")

                window2["TABLE"].update(values=libForUser.getInfoAboutUsers())

            case "Сменить пароль":
                window2.hide()
                changePassword(window2, login)
                window2["TABLE"].update(values=libForUser.getInfoAboutUsers())

            case "О программе...":
                sg.popup(
                    "Выполнила: \n Самсонова Мария Дмитриевна \n Группа А-05-21 \n Вариант 19"
                )

            case (
                "TABLE"
            ):  # Предполагаем, что этот элемент используется для выбора пользователя
                try:
                    if values["TABLE"]:
                        selected_row_index = values["TABLE"][
                            0
                        ]  # Получаем индекс выбранной строки
                        selected_row_data = rows[
                            selected_row_index
                        ]  # Получаем данные выбранной строки
                        window2["OUTPUT"].update(
                            selected_row_data[0]
                        )  # Обновляем текстовый элемен
                        window2["block"].update(
                            value=bool(
                                libForUser.getBlock(window2["OUTPUT"].get())[0][0]
                            )
                        )
                        window2["limitation"].update(
                            bool(
                                libForUser.getRestrictions(window2["OUTPUT"].get())[0][
                                    0
                                ]
                            )
                        )
                        print(selected_row_data)
                    else:
                        window2["OUTPUT"].update(
                            "No row selected"
                        )  # Или любое другое действие
                except:
                    print("log: click out")

            case "block":
                if window2["OUTPUT"].get() == "admin":
                    sg.popup("Этого пользователя невозможно заблокировать")
                elif (
                    window2["OUTPUT"].get() != "No row selected"
                    and window2["OUTPUT"].get() != ""
                ):
                    libForUser.blockUser(window2["OUTPUT"].get())
                    window2["TABLE"].update(values=libForUser.getInfoAboutUsers())

            case "limitation":
                if (
                    window2["OUTPUT"].get() != "No row selected"
                    and window2["OUTPUT"].get() != ""
                ):
                    libForUser.setLimitations(window2["OUTPUT"].get())
                    window2["TABLE"].update(values=libForUser.getInfoAboutUsers())

            case "Выход из учетной записи":
                window2.close()
                window.un_hide()
                break

            case sg.WIN_CLOSED:
                window2.close()
                window.un_hide()
                break


def mainWindowCall():
    layout = [
        [sg.Menu(menu_def)],
        [sg.Text("Имя пользователя:")],
        [sg.InputText("", key="Login")],
        [sg.Text("Пароль:")],
        [sg.InputText("", key="Password", password_char="*")],
        [sg.Button("Войти"), sg.Button("Выход")],
    ]

    # Create the Window
    window = sg.Window("Лабораторная работа номер 3", layout)

    COUNT = 0

    while True:
        event, values = window.read()

        if event == "О программе...":
            sg.popup(
                "Выполнила: \n Самсонова Мария Дмитриевна \n Группа А-05-21 \n Вариант 19"
            )
        if event == "Войти":
            window["Password"].update("")
            match libForUser.compareInput(values["Login"], values["Password"]):
                case 2:
                    sg.popup(f"Добро пожаловать {values['Login']}")
                    COUNT = 0
                    window.hide()
                    if values["Login"] == "admin":
                        windowAdminCall(
                            window, libForUser.getInfoAboutUsers(), values["Login"]
                        )
                    else:
                        windowUserCall(window, values["Login"])
                case 1:
                    COUNT += 1
                    sg.popup(
                        f"Пароль для пользователя {values['Login']} неверен\n Осталось попыток входа: {3 - COUNT}"
                    )
                case 0:
                    COUNT += 1
                    sg.popup(
                        f"Пользователя {values['Login']} не существует\n Осталось попыток входа: {3 - COUNT}"
                    )
                case 4:
                    COUNT = 0
                    sg.popup(f"Задайте пароль для пользователя {values['Login']}")
                    window.hide()
                    setNewPassword(window, values["Login"])
                case 5:
                    sg.popup(
                        f"Учетная запись пользователя {values['Login']} заблокирована\n Обратитесь к администратору"
                    )
                case 6:
                    sg.popup(
                        f"""Для учетной записи пользователя {values['Login']} введено ограничение на используемый пароль
                             \n Измените пароль!"""
                    )
                    changePassword(window, values["Login"])

        # if user closes window or clicks cancel
        if event == sg.WIN_CLOSED or event == "Выход":
            break

        if COUNT == 3 or str(values[0]) == "Выход":
            break

        print("Hello", values, "!", COUNT, type(values[0]))


if __name__ == "__main__":
    if dataBaseModule.create_and_check_database("example.db") == 1:
        print(1)
        dataBaseModule.create_scheme()
        dataBaseModule.insert_users()
    else:
        print(0)
    mainWindowCall()
