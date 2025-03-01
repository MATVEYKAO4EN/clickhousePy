import tkinter as tk
from tkinter import ttk, filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
import main

client = None
db = None
table = None
file_paths = []
def connect():
   global client
   host = entry_host.get()
   port = entry_port.get()
   username = entry_username.get()
   password = entry_password.get()
   client = main.Function.connect (host, port, username, password)
   label_connect.config(text="Подключено!")
   
def create():
   global client, db, table
   db = entry_db.get()
   table = entry_table.get()
   try:
      main.Function.createDBAndTable (client, db, table)
      label_ctreate.config(text="Создано!")
   except Exception as e:
      label_ctreate.config(text="Сначала подключитесь к ClickHouse!")

def insert():
   global client, db, table
   if client==None:
      label_insert.config(text="Сначала подключитесь к ClickHouse!")
   if db or table==None:
      label_insert.config(text="Сначала создайте бд и таблицу")
   main.Function.insert (client, file_paths, db, table)
   main.Function.count (client, db, table)
   label_insert.config(text="Успешно добавлен")

def clear():
   global client, db, table
   if client==None:
      label_insert.config(text="Сначала подключитесь к ClickHouse!")
   if db or table==None:
      label_insert.config(text="Сначала создайте бд и таблицу")
   main.Function.clearTable (client, db, table)
   label_insert.config(text="Успешно добавлен")

# Функция для обработки перетаскивания файла
def on_drop(event):
    file_path = event.data.strip('{}')  # Убираем фигурные скобки, если они есть
    entry_browse.insert(0, file_path)  # Вставляем путь в поле
    file_paths.append(fr"{file_path}")  # Добавляем путь в список

def select_file():
    file_paths_selected = filedialog.askopenfilenames()  # Выбор нескольких файлов
    if file_paths_selected:
        entry_browse.delete(0, tk.END)  # Очищаем поле
        for file_path in file_paths_selected:
            raw_file_path = fr"{file_path}"  # Преобразуем путь в "сырой" формат (r'')
            file_paths.append(raw_file_path)  # Добавляем путь в список
            entry_browse.insert(tk.END, raw_file_path + "\n")  # Вставляем путь в поле



# Создаем главное окно с поддержкой Drag and Drop
root = TkinterDnD.Tk()
root.title("Clickhouse словоформы")
root.geometry("500x400")

# Создаем Notebook (вкладки)
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Создаем три фрейма для вкладок
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
frame3 = ttk.Frame(notebook)

# Добавляем фреймы в Notebook с названиями вкладок
notebook.add(frame1, text="Подключиться к ClickHouse")
notebook.add(frame2, text="Создать БД и Таблицу")
notebook.add(frame3, text="Добавить текстовый файл")

# Содержимое первой вкладки (остается без изменений)
label_host = ttk.Label(frame1, text="Host:")
label_host.grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_host = ttk.Entry(frame1)
entry_host.grid(row=0, column=1, padx=10, pady=5)
entry_host.insert(0, "localhost")

label_port = ttk.Label(frame1, text="Port:")
label_port.grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_port = ttk.Entry(frame1)
entry_port.grid(row=1, column=1, padx=10, pady=5)
entry_port.insert(0, "8123")

label_username = ttk.Label(frame1, text="Username:")
label_username.grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_username = ttk.Entry(frame1)
entry_username.grid(row=2, column=1, padx=10, pady=5)
entry_username.insert(0, "default")

label_password = ttk.Label(frame1, text="Password:")
label_password.grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_password = ttk.Entry(frame1, show="*")
entry_password.grid(row=3, column=1, padx=10, pady=5)
entry_password.insert(0, '')

button_connect = ttk.Button(frame1, text="Подключиться", command=connect)
button_connect.grid(row=4, column=0, columnspan=2, pady=10)

label_connect = ttk.Label(frame1, text='')
label_connect.grid(row=5, column=0, columnspan=2, pady=10)

# Содержимое второй вкладки (остается без изменений)
label_db = ttk.Label(frame2, text="Название БД:")
label_db.grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_db = ttk.Entry(frame2)
entry_db.grid(row=0, column=1, padx=10, pady=5)
entry_db.insert(0, "DBWordForm")

label_table = ttk.Label(frame2, text="Название таблицы:")
label_table.grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_table = ttk.Entry(frame2)
entry_table.grid(row=1, column=1, padx=10, pady=5)
entry_table.insert(0, "form_table")

button_create = ttk.Button(frame2, text="Создать", command=create)
button_create.grid(row=2, column=0, columnspan=2, pady=10)

label_ctreate = ttk.Label(frame2, text='')
label_ctreate.grid(row=3, column=0, columnspan=2, pady=10)

# Содержимое третьей вкладки
# Поле для перетаскивания файла
entry_drag = ttk.Label(frame3, width=40,text="Перетащите файл сюда",borderwidth=2, relief="solid", padding=(10,50))
entry_drag.grid(row=0, column=1, padx=10, pady=5)
entry_drag.drop_target_register(DND_FILES)
entry_drag.dnd_bind('<<Drop>>', on_drop)

# Поле для выбора файла через проводник
label_browse = ttk.Label(frame3, text="Выберите файл:")
label_browse.grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_browse = ttk.Entry(frame3, width=40)
entry_browse.grid(row=1, column=1, padx=10, pady=5)
button_browse = ttk.Button(frame3, text="Обзор", command=select_file)
button_browse.grid(row=1, column=2, padx=10, pady=5)

# Кнопка "Путь получен"
button_path = ttk.Button(frame3, text="Добавить", command=insert)
button_path.grid(row=2, column=0, columnspan=3, pady=20)

# Кнопка "Путь получен"
button_path = ttk.Button(frame3, text="Очистить таблицу", command=clear)
button_path.grid(row=3, column=0, columnspan=3, pady=20)

# Комент
label_insert = ttk.Label(frame3, text='')
label_insert.grid(row=4, column=0, columnspan=2, pady=10)

# Запускаем главный цикл обработки событий
root.mainloop()