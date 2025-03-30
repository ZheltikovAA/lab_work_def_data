import PySimpleGUI as sg
import main


def windowAdminCall():
    layoutToAdmin = [    
        [sg.Menu(main.menu_def)],
        [sg.Button('Выход из учетной записи')] 
        ]

    window2 = sg.Window('Административная панель', layoutToAdmin)
    while True:
        event, values = window2.read()

        if event == sg.WIN_CLOSED or event == 'Выход из учетной записи':
            window2.close()
            main.window.un_hide()
            break

