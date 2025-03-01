## Описание
Используя python и библиотеку clickhouse-connect<br/>  Реализовал локальное подключение к clickhouse.
## Созданные функции

connect (host, port, username, password) - функция для подключения к бд.<br/>
createDBAndTable (client, db, table) - создает бд и таблицу если их нет с 2 параметрами wordform - словоформы, amt - количество повторений.<br/>
insert (client, file_paths, db, table) - функция вставки словоформ в бд из нескольких файлов ( вставляеться строка 'wordform','1').<br/>
count (client, db, table) - функция подсчёта повторений и удаления дублей.<br/>
clearTable (db, table) - функция для очистки таблицы.

## Структура бд
Таблица form_table
| wordform | amt |
|---------:|-----|
| Michel   | 1   |
| Mon      | 10  |
| Так      | 18  |
# Example headings
