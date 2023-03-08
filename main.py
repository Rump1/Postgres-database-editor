import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def autorization(): # Функция, отвечающая за стартовое окно с авторизацией
    autorization_window.geometry('490x170')     # Установка размера окна
    autorization_window.title("Авторизация")     # Название окна
    autorization_window.config(bg="gray90")        # Цвет фона

    autorization_frame = tk.LabelFrame(autorization_window, text="Введите данные для соединения с БД", font=("Arial", 11), labelanchor="n", bg="gray95")     # Рамка с полями авторизации
    autorization_frame.pack(padx=10, pady=5, fill="both", ipadx=5, ipady=5)

    user_label = tk.Label(autorization_frame, text="user", font=("Arial", 11), width=25)    # Текст "user"
    user_label.grid(row=0, column=0, sticky="S")
    user_entry = tk.Entry(autorization_frame, width=20)     # Поле для ввода user
    user_entry.grid(row=1, column=0, sticky="N")

    pwd_label = tk.Label(autorization_frame, text="password", font=("Arial", 11), width=25)     # Текст "password"
    pwd_label.grid(row=0, column=1, sticky="S")
    pwd_entry = tk.Entry(autorization_frame, width=20)     # Поле для ввода password
    pwd_entry.grid(row=1, column=1, sticky="N")

    host_label = tk.Label(autorization_frame, text="host", font=("Arial", 11), width=25)    # Текст "host"
    host_label.grid(row=3, column=0, sticky="S")
    host_entry = tk.Entry(autorization_frame, width=20)     # Поле для ввода host
    host_entry.grid(row=4, column=0, sticky="N")

    port_label = tk.Label(autorization_frame, text="port", font=("Arial", 11), width=25)    # Текст "port"
    port_label.grid(row=3, column=1, sticky="S")
    port_entry = tk.Entry(autorization_frame, width=20)     # Поле для ввода port
    port_entry.grid(row=4, column=1, sticky="N")
    '''
    В параметр command для кнопки можно запихать лямбда функцию, чтобы использовать эту функцию с параметрами.
    Таким образом происходит передача заполненных пользователем данных
    '''
    connect_button = tk.Button(autorization_window, text="Войти", font=("Arial", 11), width=20,
                               command=lambda: enter_button(user_entry.get(), host_entry.get(), pwd_entry.get(), port_entry.get()))
    connect_button.pack()

    autorization_window.mainloop()

def enter_button(_user, _host, _password, _port):   # Действия, происходящие после нажатия кнопки "Войти"
    try:
        # Подключение к существующей базе данных
        global connection
        connection = psycopg2.connect(user=_user, password=_password, host=_host, port=_port)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        global user     # Изменение значений глобальных переменных для будушего использования
        user = _user
        global password
        password = _password
        global port
        port = _port
        global host
        host = _host
        start_main_window()
    except (Exception, Error) as error:
        error_message(error)

def error_message(error):
    mb.showerror("Ошибка", error)

def success_message():
    mb.showinfo("Информация", "Операция прошла успешно!")




def start_main_window():
    autorization_window.withdraw()
    main_window = tk.Toplevel(width=480, height=370, bg="gray90")   # Инициализация окна
    main_window.title("dbPostgresEditor")    # Название окна
    main_window.protocol("WM_DELETE_WINDOW", lambda: autorization_window.destroy())
        #Рамка коннекта к бд
    connect_frame = tk.LabelFrame(main_window, text="Соединение с базой данных", font=("Arial", 11), labelanchor="n", bg="gray95")     #Рамка присоединения к БД
    connect_frame.pack(padx=10, pady=5, fill="x")

    connect_to_db_message = tk.Label(connect_frame, text="Выберите БД из списка ниже", font=("Arial", 11), width=25)
    connect_to_db_message.grid(row=0, column=0, sticky="S", pady=5)

    connect_to_db_button = tk.Button(connect_frame, text = "Соединиться с БД", font=("Arial", 11), width=19, command=lambda: connect_to_db(combobox.get(), table_listbox, main_window))     #Кнопка подключения к БД
    connect_to_db_button.grid(row=1, column=1, padx=27, pady=5)

    create_new_db_button = tk.Button(connect_frame, text = "Создать новую БД", font=("Arial", 11), width=19, command=lambda: create_new_db(combobox, main_window))     #Кнопка создания новой БД
    create_new_db_button.grid(row=0, column=1, padx=27, pady=5)

        #Рамка редактирования таблиц БД
    table_edit_frame = tk.LabelFrame(main_window, text = "Редактирование таблиц в БД", font=("Arial", 11), labelanchor="n", bg = "gray95")      #Рамка редактирования таблиц
    table_edit_frame.pack(padx=10,pady=10, fill="both", expand="yes")

    connect_to_db_message = tk.Label(table_edit_frame, text="Список таблиц", font=("Arial", 11), width=25)      #Надпись "Список таблиц"
    connect_to_db_message.grid(row=0, column=0, sticky="S", pady=5)

    table_listbox = tk.Listbox(table_edit_frame)    #Размещение листбокса в гриде
    table_listbox.grid(row=1, column=0, rowspan=3, sticky="news", padx=5)

    scrollbar = tk.Scrollbar(table_edit_frame)     #Размещение скроллбара в гриде
    scrollbar.grid(row=1, column=1, rowspan=3, sticky="nws")

    table_listbox.config(yscrollcommand=scrollbar.set)     #Прикрепление скроллбара к листбоксу
    scrollbar.config(command=table_listbox.yview)

    edit_table_button = tk.Button(table_edit_frame, text="Редактировать таблицу", font=("Arial", 11), command=lambda: edit_table(table_listbox, table_listbox.get(table_listbox.curselection()) if table_listbox.curselection() else ""))
    edit_table_button.grid(row=1, column=2, sticky="e", padx=10)

    delete_table_button = tk.Button(table_edit_frame, text = "Удалить таблицу", font=("Arial", 11), width=19, command=lambda: delete_table(table_listbox))
    delete_table_button.grid(row=2, column=2, sticky="e", padx=10)

    create_new_table_button = tk.Button(table_edit_frame, text = "Создать таблицу", font=("Arial", 11), width=19, command=lambda: create_table(table_listbox))
    create_new_table_button.grid(row=3, column=2, sticky="e", padx=10)

    global connection
    cursor = connection.cursor()
    sql_get_databases = "select datname from pg_database where datname not in ('template1', 'template0')" # Запрос на получение всех БД на сервере
    cursor.execute(sql_get_databases)
    list_for_combobox = cursor.fetchall()

    combobox = ttk.Combobox(connect_frame, width=30, values=list_for_combobox, state="readonly")  # Комбобокс для выбора БД для подключения
    combobox.grid(row=1, column=0, padx=5, pady=5)  # Размещение комбобокса в рамке

    main_window.mainloop()

def create_new_db(combobox, main_window):   # Функция кнопки "Создать новую БД"
    create_db_window = tk.Toplevel(width=480, height=370, bg="gray90")   # Инициализация окна
    create_db_window.title("Создание БД")    # Название окна
    db_name_label = tk.Label(create_db_window, text="Введите название БД", font=("Arial", 11), width=25, bg="gray90")    # Текст
    db_name_label.grid(row=0, column=0, sticky="S", padx=10, pady=5)
    db_name_entry = tk.Entry(create_db_window, width=20)     # Поле для ввода
    db_name_entry.grid(row=1, column=0, sticky="N", padx=10, pady=5)
    access_button = tk.Button(create_db_window, text="Принять", font=("Arial", 11), width=10, command=lambda: access_button_fucn(create_db_window, db_name_entry.get(), combobox, main_window))
    access_button.grid(row=2, column=0, sticky="S", padx=10, pady=5)

def access_button_fucn(window, dbname, combobox, main_window):      # Функция кнопки "Принять" в окне создания БД
    global connection
    if connection:
        connection.close()
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user=user, password=password, host=host, port=port)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        sql_create_database = 'create database  ' + dbname   # Запрос на создание БД
        cursor.execute(sql_create_database)     # Выполнение запроса
        combobox['values'] = tuple(list(combobox['values']) + [dbname])     # Добавление названия БД в комбобокс
        main_window.update()
        window.destroy()    # Закрытие окна
        success_message()   # Всплывающее окно об успехе операции
    except (Exception, Error) as error:
        error_message(error)
def connect_to_db(db_name, table_listbox, main_window):     # Функция кнопки "Подключиться к БД"
    global connection
    if connection:
        connection.close()
    if (db_name == ""):
        error_message("Выберите базу данных из списка")
    else:
        try:
            # Подключение к существующей базе данных
            connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=db_name)
            cursor = connection.cursor()
            sql_get_tables = "select table_name from information_schema.tables where table_schema = 'public';" # Получаем список таблиц в БД
            cursor.execute(sql_get_tables)     # Выполнение запроса
            table_list = cursor.fetchall()     # Сохранение данных с запроса
            table_listbox.delete(0, table_listbox.size()-1)      # Очистка значений в списке таблиц
            for item in table_list:
                table_listbox.insert("end", item)   # Добавление значений в списке таблиц
            main_window.update()    # Обновление окна
            global is_connected
            is_connected = True
            success_message()   # Сообщение об успешности операции
        except (Exception, Error) as error:
            error_message(error)


def create_table_widgets(table_listbox, window, mode, table_name):    # Функция создания виджетов для окна создания и редактирования таблиц
    field_entry_title = tk.Label(window, text="Имя поля", bg="gray90", font=("Arial", 11))      # Текст "Имя поля"
    field_entry_title.grid(row=0, column=0, padx=6, sticky="ews")

    field_type_title = tk.Label(window, text="Тип поля", bg="gray90", font=("Arial", 11))      # Текст "Тип поля"
    field_type_title.grid(row=0, column=1, padx=6, sticky="ews")

    field_entry = tk.Entry(window)     # Поле для ввода имени поля
    field_entry.grid(row=1, column=0, padx=6, pady=6, sticky="ewn")

    field_type_combobox = ttk.Combobox(window, state="readonly", width=18, values=["int", "real", "varchar", "timestamp"])
    field_type_combobox.grid(row=1, column=1, padx=6, pady=6, sticky="ewn")     # Комбобокс для выбор типа поля

    field_listbox = tk.Listbox(window)      # листбокс для вывода существующих в таблице полей
    field_listbox.grid(row=2, column=0, columnspan=2, rowspan=2, sticky="ew", padx=5, pady=5)
    if (mode == "edit"):    # Если редактируем таблицу
        cursor = connection.cursor()    # Создаем курсор
        sql_get_fields = f"select column_name, data_type from information_schema.columns where table_name = '{table_name}';"    # Запрос получения всех полей и их типов в таблице
        cursor.execute(sql_get_fields)      # Выполнение запроса
        fields = cursor.fetchall()      # Записываем результат, представленный в виде списка кортежей вида (field_name, field_type)
        for item in fields:
            field_listbox.insert("end", item[0] + " " + item[1])    # Добавляем элементы в листбокс

    add_field_button = tk.Button(window, text="Добавить поле", width=15, command=lambda: add_field_in_create_table(field_entry.get(), field_type_combobox.get(), field_listbox), font=("Arial", 11))
    add_field_button.grid(row=1, column=2, padx=6, pady=6, sticky="n")      # Кнопка "Добавить поле"
    if (mode == "edit"):    # Если мы открываем окно редактирования, то меняем функцию у кнопки
        add_field_button['command'] = lambda: add_field_in_edit_table(field_entry.get(), field_type_combobox.get(), field_listbox, table_name)

    delete_field_button = tk.Button(window, text="Удалить поле", command=lambda: delete_field_in_create_table(field_listbox, table_name), font=("Arial", 11), width=15)
    delete_field_button.grid(row=2, column=2, padx=5, pady=5)       # Кнопка "Удалить поле"
    if (mode == "edit"):     # Если мы открываем окно редактирования, то меняем функцию у кнопки
        delete_field_button['command'] = lambda: delete_field_in_edit_table(field_listbox, table_name)

    key_field_label = tk.Label(window, text="Ключевое поле не выбрано", bg="gray90", font=("Arial", 9))
    key_field_label.grid(row=4, column=0, padx=6, sticky="ws", columnspan=3)     # Label для отображения названия ключевого поля
    if (mode == "edit"):    # Если мы открываем окно редактирования, то список полей и ключевое поле должны быть уже выбраны
        cursor = connection.cursor()
        sql_get_tables = f'''SELECT c.column_name, c.data_type FROM information_schema.table_constraints tc 
                            JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name) 
                            JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema 
                            AND tc.table_name = c.table_name AND ccu.column_name = c.column_name 
                            WHERE constraint_type = 'PRIMARY KEY' and tc.table_name = '{table_name}' ''' # Получаем название и тип ключевого поля
        cursor.execute(sql_get_tables)  # Выполнение запроса
        key_field = cursor.fetchall()    # Курсор вернет список из одного элемента, который является кортежом
        if (key_field):
            key_field = key_field[0][0] + " " + key_field[0][1]
            key_field_label['text'] = f"Ключевым полем является {key_field}"    # Если имеем дело с уже созданной таблицей, меняем сообщение о ключевом поле

    set_key_field_button = tk.Button(window, text="Сделать ключевым", command=lambda: set_key_field_in_create_table(key_field_label, field_listbox), font=("Arial", 11), width=15)
    set_key_field_button.grid(row=3, column=2, padx=5, pady=5)      # Кнопка для выбора ключевого поля
    if (mode == "edit"):    # Если мы открываем окно редактирования, то меняем функцию у кнопки
        set_key_field_button['command'] = lambda: set_key_field_in_edit_table(key_field_label, field_listbox, table_name)

    table_name_label = tk.Label(window, text="Введите имя таблицы:", bg="gray90", font=("Arial", 11))
    table_name_label.grid(row=5, column=0, padx=6, pady=6, sticky="ew")     # Текст "Введите имя таблицы"

    table_name_entry = tk.Entry(window)     # Поле для ввода имени таблицы
    table_name_entry.grid(row=5, column=1, padx=6, pady=6, sticky="ew")

    create_table_finish_button = tk.Button(window, text="Готово", width=13, command=lambda: finish_create_table_in_create_table(window, table_name_entry.get(), field_listbox, key_field_label, table_listbox), font=("Arial", 11))
    create_table_finish_button.grid(row=5, column=2, padx=5, pady=5)        # Кнопка "Готово"
    if (mode == "edit"):    # Если мы открываем окно редактирования, то меняем функцию у кнопки
        create_table_finish_button['command'] = lambda: finish_create_table_in_edit_table(window, table_name_entry.get(), table_listbox, table_listbox.get(table_listbox.curselection())[0], table_listbox.curselection())

def create_table(listbox):     #   Функция кнопки "Создать таблицу"
    if (is_connected):
        create_table_window = tk.Toplevel(width=350, height=300, bg="gray90")      # Создаем новое окно
        create_table_window.title("Создание новой таблицы")     # Настраиваем его параметры
        create_table_window.columnconfigure(index=0, weight=4)     # Изменение весов строк и столбцов
        create_table_window.rowconfigure(index=2, weight=3)
        create_table_widgets(listbox, create_table_window, "create", " ")    # Вызываем функцию создания виджетов
        create_table_window.mainloop()      # Цикл работы с окном
    else:
        error_message("Пожалуйста, подключитесь к БД")

def add_field_in_create_table(text, type, listbox):
    if (not text):      # Проверка на ввод имени поля
        error_message("Введите имя поля")
    elif (not type):       # Проверка на ввод типа поля
        error_message("Выберите тип поля")
    elif (" " in text):
        error_message("В названии поля есть пробелы. Попробуйте еще раз")
    elif(text + " " + type in listbox.get(0, listbox.size()-1)):      # Проверка на наличие поля в листбоксе
        error_message("Такое поле уже существует")
    else:
        listbox.insert("end", text + " " + type)
        print(listbox.size())

def delete_field_in_create_table(listbox, table_name):
    if (listbox.curselection()):
        listbox.delete(listbox.curselection())
    else:
        error_message("Выберите поле для удаления из списка")

def set_key_field_in_create_table(label, listbox):
    if (listbox.curselection()):
        label['text'] = "Ключевым полем является " + listbox.get(listbox.curselection())
        label.update()
    else:
        error_message("Выберите ключевое поле")


def finish_create_table_in_create_table(window, table_name, field_listbox, label, tables_listbox):
    if (not table_name):
        error_message("Введите имя таблицы")
    elif (label['text'] == "Ключевое поле не выбрано"):
        error_message("Выберите ключевое поле")
    else:
        try:
            label_text_list = label['text'].split()     # Получаем текст из лейбла и переводим в список
            key_field = label_text_list[3] + " " + label_text_list[4]       # Находим там ключевое поле
            fields_list = list(field_listbox.get(0, field_listbox.size()-1))       # Формируем список всех полей из кортежа
            fields_list[fields_list.index(key_field)] += " primary key"     # Добавляем текст " primary key" к ключевому полю
            cursor = connection.cursor()        # Инициализация курсора
            sql_create_table = f'create table  "{table_name}" ({", ".join(fields_list)})'      # Формируем запрос
            cursor.execute(sql_create_table)    # Выполняем запрос
            tuple = (table_name,)   # Переводим название таблицы в кортеж(в листбоксе они хранятся в кортеже кортежей)
            tables_listbox.insert("end", tuple)    # Добавляем название таблицы в table_listbox
            window.destroy()
            connection.commit()     # Коммитим изменения в БД
            success_message()       # Выдаем сообщение о успешном выполнении
        except (Exception, Error) as error:
            error_message(error)
            connection.rollback()      # Отменяем всю транзакцию в случае неудачи


def edit_table(table_listbox, table_name):   # Функция кнопки "Редактировать таблицу"
    if (not table_name):
        error_message("Выберите таблицу")
    elif (is_connected):
        table_name = table_name[0]
        edit_table_window = tk.Toplevel(width=350, height=300, bg="gray90")  # Создаем новое окно
        edit_table_window.title("Редактирование таблицы")  # Настраиваем его параметры
        edit_table_window.columnconfigure(index=0, weight=4)  # Изменение весов строк и столбцов
        edit_table_window.rowconfigure(index=2, weight=3)
        create_table_widgets(table_listbox, edit_table_window, "edit", table_name)  # Вызываем функцию создания виджетов
        edit_table_window.mainloop()  # Цикл работы с окном
    else:
        error_message("Пожалуйста, подключитесь к БД")

def add_field_in_edit_table(text, type, listbox, table_name):
    if (not text):  # Проверка на ввод имени поля
        error_message("Введите имя поля")
    elif (not type):  # Проверка на ввод типа поля
        error_message("Выберите тип поля")
    elif (" " in text):
        error_message("В названии поля есть пробелы. Попробуйте еще раз")
    elif (text + " " + type in listbox.get(0, listbox.size() - 1)):  # Проверка на наличие поля в листбоксе
        error_message("Такое поле уже существует")
    else:
        try:
            cursor = connection.cursor()  # Инициализация курсора
            sql_add_field = f'alter table "{table_name}" add column {text} {type}'  # Формируем запрос
            cursor.execute(sql_add_field)  # Выполняем запрос
            connection.commit()  # Коммитим изменения в БД
            listbox.insert("end", text + " " + type)    # Добавляем поле в листбокс
        except (Exception, Error) as error:
            error_message(error)
            connection.rollback()      # Отменяем всю транзакцию в случае неудачи

def delete_field_in_edit_table(field_listbox, table_name):
    if (field_listbox.curselection()):    # Если выбрано поле
        try:
            field_name = field_listbox.get(field_listbox.curselection()).split()[0]   # get вернет строку вида (field_name field_type), нам надо получить field_name
            cursor = connection.cursor()        # Инициализация курсора
            sql_delete_field = f'alter table {table_name} drop column {field_name};'    # Запрос на удаление поля
            cursor.execute(sql_delete_field)    # Выполнение запроса
            connection.commit()     # Коммитим изменения
            field_listbox.delete(field_listbox.curselection())  # Удаляем поле из листбокса
        except (Exception, Error) as error:
            error_message(error)
            connection.rollback()  # Отменяем всю транзакцию в случае неудачи
    else:
        error_message("Выберите поле для удаления из списка")

def set_key_field_in_edit_table(label, field_listbox, table_name):
    if (field_listbox.curselection()):  # Если выбрано поле
        try:
            field_name = field_listbox.get(field_listbox.curselection()).split()[0] # get вернет строку вида (field_name field_type), нам надо получить field_name
            cursor = connection.cursor()    # Инициализация курсора
            sql_set_key_field = f'''alter table {table_name} drop constraint {table_name}_pkey;     
                                    alter table {table_name} add primary key ({field_name});''' # Запрос на смену ключевого поля. Снимается старое, назначается новое
            cursor.execute(sql_set_key_field)   # Выполнение запроса
            connection.commit()     # Коммитим изменения
            label['text'] = "Ключевым полем является " + field_listbox.get(field_listbox.curselection())  # Сменяем информацию в отображении ключевого поля
            label.update()
        except (Exception, Error) as error:
            error_message(error)
            connection.rollback()  # Отменяем всю транзакцию в случае неудачи
    else:
        error_message("Выберите поле для удаления из списка")

def finish_create_table_in_edit_table(window, new_table_name, tables_listbox, table_name, table_name_index):
    if (not new_table_name):    # Если имя таблицы стерто
        error_message("Введите имя таблицы")    # Выдаем ошибку
    elif (new_table_name != table_name):     # Если введено новое имя для таблицы
        try:
            cursor = connection.cursor()       # Инициализация курсора
            sql_rename = f'alter table {table_name} rename to {new_table_name};'    # Запрос на переименование таблицы
            cursor.execute(sql_rename)      # Выполнение запроса
            connection.commit()
            tables_listbox.delete(table_name_index)    # Удаление старой таблицы из листбокса
            tuple = (new_table_name,)
            tables_listbox.insert("end", tuple)        # Добавление новой
            window.destroy()
        except (Exception, Error) as error:
            error_message(error)
            connection.rollback()  # Отменяем всю транзакцию в случае неудачи

def delete_table(table_listbox):     # Функция кнопки "Удалить таблицу"
    if (table_listbox.curselection()):  # Если таблица выбрана
        table_index = table_listbox.curselection()  # Получаем индекс таблицы
        table_name = table_listbox.get(table_index)[0]      # Получаем имя таблицы
        try:
            cursor = connection.cursor()    # Инициализация курсора
            sql_delete_table = f'drop table "{table_name}"'   # Запрос на удаление
            cursor.execute(sql_delete_table)    # Выполнение запроса
            connection.commit()     # Коммит изменений
            table_listbox.delete(table_index)   # Удаление таблицы из листбокса
        except (Exception, Error) as error:
            error_message(error)
            connection.rollback()  # Отменяем всю транзакцию в случае неудачи
    else:
        error_message("Выберите таблицу")

autorization_window = tk.Tk()   # Инициализация окна
user = ""       # Данные для авторизации
host = ""
password = ""
port = ""
connection = ""
is_connected = False
autorization()

