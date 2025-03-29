## Описание
Используя python и библиотеку clickhouse-connect<br/>  Реализовал локальное подключение к clickhouse.
Для запуска приложения использовать runApp.py
### Тест работы приложения
![Alt text](/imageForReadMeFolder/4.jfif)<br/>
![Alt text](/imageForReadMeFolder/5.png)<br/>
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

## Создал простой графический интерфейс
Состоящий из трех окон<br/>
Первое окно с полями для подключения к clickhouse<br/>
![Alt text](/imageForReadMeFolder/1frame.png?raw=true "Optional Title")<br/>
<br/>
<br/>
Второе окно для создания бд и таблицы<br/>
![Alt text](/imageForReadMeFolder/2frame.png?raw=true "Optional Title")<br/>
<br/>
<br/>
Третье окно для добавления файлов<br/>
![Alt text](/imageForReadMeFolder/3frame.png?raw=true "Optional Title")<br/>
<br/>
<br/>
Третье окно подтверждение удаления<br/>
![Alt text](/imageForReadMeFolder/31frame.png?raw=true "Optional Title")<br/>