Используя python и библиотеку clickhouse-connect 
Реализовал локальное подключение к clickhouse
Создал 5 функции:
  connect(host,port,username,password) - функция для подключения к бд.
  createDBandTable(client,db,table) - создает бд и таблицу если их нет с 2 параметрами wordform - словоформы, amt - количество повторений.
  insert(client, file_paths, db, table) - функция вставки словоформ в бд из нескольких файлов ( вставляеться строка 'wordform','1').
  count(client,db,table) - функция подсчёта повторений и удаления дублей.
  clearTable(db,table) - функция для очистки таблицы.
  
