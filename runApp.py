import tkinter as tk
from tkinter import ttk, filedialog,messagebox 
from tkinterdnd2 import TkinterDnD, DND_FILES
import main
import time
import threading
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Доступ к данным
db_config = config["database_config"]
host = db_config["host"]
port = db_config["port"]
username = db_config["username"]
database = db_config["database"]
table = db_config["table"]
client = None
#сохранение настроек
def save_config():
    config = {
       "database_config": {
            "host": entry_host.get(),
            "port": entry_port.get(),
            "username": entry_username.get(),
            "database": entry_database.get(),
            "table": entry_table.get()
        }
    }
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    print("Данные сохранены в config.json")
    

file_paths = []
def connect():
   host = entry_host.get()
   port = entry_port.get()
   username = entry_username.get()
   password = entry_password.get()
   save_config()

   label_connect.config(text="Подключение...", foreground="blue")

   # Запускаем подключение в отдельном потоке
   threading.Thread(
      target=try_connect,
      args=(host, port, username, password),
      daemon=True  # Поток завершится при закрытии программы
   ).start()

def try_connect(host, port, username, password):
    global client
    try:
        client = main.Function.connect(host, port, username, password)
        client.query("SELECT 1")  # Проверка соединения
        # Обновляем GUI из главного потока
        label_connect.after(0, lambda: label_connect.config(text="Подключено!", foreground="green"))
    except Exception as e:
        label_connect.after(0, lambda: label_connect.config(text=f"Ошибка подключения", foreground="red"))
        client = None
   
def create():
   global client
   database = entry_database.get()
   table = entry_table.get()
   save_config()
   try:
      main.Function.createDBAndTable (client, database, table)
      label_ctreate.config(text="Создано!",foreground="green")
   except Exception as e:
      label_ctreate.config(text="Сначала подключитесь к ClickHouse!")

def insert():
    global client
    database = entry_database.get()
    table = entry_table.get()
    
    # Проверка подключения и выбора БД/таблицы
    if client is None:
        label_insert.config(text="Сначала подключитесь к ClickHouse!")
        return
    if not database or not table:
        label_insert.config(text="Сначала создайте БД и таблицу!")
        return
    if not file_paths:  # Проверка на пустой путь к файлу
        label_insert.config(text="Укажите файл для загрузки!")
        return
    
    # Меняем текст и цвет для индикации начала обработки
    label_insert.config(text="Обработка файла...", foreground="blue")
    
    # Запуск обработки в отдельном потоке
    threading.Thread(
        target=process_insert, 
        daemon=True  # Поток завершится при закрытии программы
    ).start()

def process_insert():
    try:
        timeStart = time.time()
        
        # Вставляем данные
        main.Function.insert(client, file_paths, database, table)
        
        # Обновляем счетчик
        main.Function.count(client, database, table)
        
        timeEnd = time.time()
        
        # Обновляем GUI из основного потока
        label_insert.after(0, lambda: label_insert.config(
            text=f"Успешно добавлено, время: {timeEnd-timeStart:.2f} сек",
            foreground="green"
        ))
        
    except Exception as e:
        # Вывод ошибки в GUI
        label_insert.after(0, lambda: label_insert.config(
            text=f"Ошибка: {str(e)}",
            foreground="red"
        ))

def clear():
    global client, database, table
    
    # Проверка условий
    if client is None:
      label_insert.config(text="Сначала подключитесь к ClickHouse!")
      return
        
    if database is None or table is None:
      label_insert.config(text="Сначала создайте бд и таблицу")
      return
    
    # Диалог подтверждения
    confirm = messagebox.askyesno(
        title="Подтверждение",
        message="Вы уверены, что хотите очистить таблицу?",
        icon='warning'
    )
    
    if confirm:  # Если пользователь нажал "Да"
        try:
            main.Function.clearTable(client, database, table)
            label_insert.config(text="Таблица успешно очищена")
        except Exception as e:
            label_insert.config(text=f"Ошибка: {str(e)}")
    else:
        label_insert.config(text="Действие отменено")

# Функция для обработки перетаскивания файла
def on_drop(event):
   file_paths_selected = [file_paths.replace("{", "").replace("}", "") for file_paths in event.data.split('} {')]
   if file_paths_selected:
      entry_browse.delete(0, tk.END)
      for file_path in file_paths_selected:
         file_paths.append(fr"{file_path}")  # Добавляем путь в список
         entry_browse.insert(tk.END, file_path+" ")  # Вставляем путь в поле

def select_file():
   file_paths_selected = filedialog.askopenfilenames()  # Выбор нескольких файлов
   if file_paths_selected:
      entry_browse.delete(0, tk.END)
      for file_path in file_paths_selected:
         file_paths.append(fr"{file_path}")
         entry_browse.insert(tk.END, file_path+" ") 

# Описание графического интерфейса
# Создаем главное окно с поддержкой Drag and Drop
root = TkinterDnD.Tk()
root.title("Clickhouse словоформы")
x = (root.winfo_screenwidth() // 2) - 250
y = (root.winfo_screenheight() // 2) - 200
root.geometry(f"500x400+{x}+{y}")
root.resizable(False, False)
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

# Содержимое первой вкладки
label_host = ttk.Label(frame1, text="Host:")
label_host.grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_host = ttk.Entry(frame1)
entry_host.grid(row=0, column=1, padx=10, pady=5)
entry_host.insert(0, host)

label_port = ttk.Label(frame1, text="Port:")
label_port.grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_port = ttk.Entry(frame1)
entry_port.grid(row=1, column=1, padx=10, pady=5)
entry_port.insert(0, port)

label_username = ttk.Label(frame1, text="Username:")
label_username.grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_username = ttk.Entry(frame1)
entry_username.grid(row=2, column=1, padx=10, pady=5)
entry_username.insert(0, username)

label_password = ttk.Label(frame1, text="Password:")
label_password.grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_password = ttk.Entry(frame1, show="*")
entry_password.grid(row=3, column=1, padx=10, pady=5)
entry_password.insert(0, '')

button_connect = ttk.Button(frame1, text="Подключиться", command=connect)
button_connect.grid(row=4, column=0, columnspan=2, pady=10)

label_connect = ttk.Label(frame1, text='')
label_connect.grid(row=5, column=0, columnspan=2, pady=10)

# Содержимое второй вкладки
label_db = ttk.Label(frame2, text="Название БД:")
label_db.grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_database = ttk.Entry(frame2)
entry_database.grid(row=0, column=1, padx=10, pady=5)
entry_database.insert(0, database)

label_table = ttk.Label(frame2, text="Название таблицы:")
label_table.grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_table = ttk.Entry(frame2)
entry_table.grid(row=1, column=1, padx=10, pady=5)
entry_table.insert(0, table)

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