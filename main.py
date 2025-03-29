import clickhouse_connect

class Function(object):
    def connect (host, port, username, password):
        client = clickhouse_connect.get_client(host=host, port=port, username=username, password=password)
        print("подключено!")
        return client

    def createDBAndTable (client, db, table):
        client.command(f'CREATE DATABASE IF NOT EXISTS {db}')

        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {db}.{table} (
            wordform String,
            amt UInt32
        ) ENGINE = MergeTree
        ORDER BY tuple();
        '''
        client.command(create_table_query)
        print("Создано!")

    def insert (client, file_paths, db, table):
        batch_size = 1000000  # Размер батча

        # Функция для вставки батча
        def insert_batch(batch):
            if batch:
                client.insert(f'{db}.{table}', batch, column_names=['wordform', 'amt'])
                
        #cтрока храняшая символы для замены
        chars_to_replace = "()?!;:.,"
        translation_table = str.maketrans(chars_to_replace, ' ' * len(chars_to_replace))
        # Чтение файлов и вставка данных
        for file_path in file_paths:  
            batch = []
            
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    
                    line = line.translate(translation_table)
                    wordforms = line.strip().split()
                    batch.extend([(wordform, 1) for wordform in wordforms])

                    # Если батч достиг размера batch_size, вставляем его
                    if len(batch) >= batch_size:
                        insert_batch(batch)
                        batch = []  # Очищаем батч после вставки

                # Вставляем оставшиеся данные (последний батч)
                if batch:  # Проверяем, что батч не пустой
                    insert_batch(batch)
        print("Все файлы успешно вставлены.")

    def count (client, db, table):
        # SQL-запрос для группировки и суммирования
        query = f"""
        SELECT wordform, SUM(amt) AS total_amt
        FROM {db}.{table}
        GROUP BY wordform
        """

        # Выполнение запроса
        result = client.query(query)

        # Получение результатов
        grouped_data = result.result_set

        # Удаление старых данных и вставка новых
        client.command(f"TRUNCATE TABLE {db}.{table}")

        insert_query = f"INSERT INTO {db}.{table} (wordform, amt) VALUES"
        values = [(row[0], row[1]) for row in grouped_data]
        client.insert(f"{db}.{table}", values, column_names=['wordform', 'amt'])

        print("Данные успешно обновлены.")

    def clearTable (client, db, table):
        # Очистка таблицы
        client.command(f'TRUNCATE TABLE {db}.{table}')
        print(f"Таблица {db}.{table} успешно очищена.")

if __name__ == "__main__":
    fun=Function()
    host ='localhost'
    port='8123'
    username='default'
    password=''
    database='DBWordForm'
    table='form_table'
    file_paths = [
    r'Война и мир\Война и мир.txt'
]
    # Подключение к ClickHouse
    client =  fun.connect ( host, port, username, password)
    
    # Создание базы данных и таблицы
    # fun.createDBAndTable (client, database, table)


    # Вставка данных из файла
    fun.insert (client, file_paths, database, table)
    
    # Подсчёт количества строк в таблице
    fun.count (client, database, table)

    # # #Очистить таблицу
    # fun.clearTable (client, database, table)