# ****Telegram-Dialog

* [X] Написать процедуру, которая запускает ботов и читает чаты в поисках новых сообщений, но пока просто celery  задача на ежедневный парсинг сообщени
* [ ] напиши анализ ролей в каждом source (были выписаны пользователи, колл-во сообщений суммарное и колл-во сообщений за неделею )
* [ ] Написать логику между диалогом и source(как должны создаваться сцены для drain)
* [X] заново пересмотреть алгоритм генерации диалогов
* [X] сделать фильтрацию диалогов по тегам
* [X] cделать генерацию сцен из диалогов автоматически
* [X] сделать очистку повторяющихся сообщений
* [X] cделать фильтрацию сообщений по группе
* [ ] добавить в телеграмдиалог поля активности диалога в админку
* [ ] перенести груупу и время старта в модель диалога
* [X] переписать активность связь групп =
* [ ] добавить в дилаоги коллво сообщений
* [ ] нагенерировать диалоги для 1 моего чата (Грузия)
* [ ] добавить watch в докер
* [X] Добавить индекс везде где есть поиск
* [ ] добавит уникальные поля constrains там где должны быть уникальные поля (Messages, Role
* [ ] Добавить валидацию для Messages чтобы поле reply_to msg могло ссылаться на сообщение из одного и тогоже диалога
* [ ] Добавить фильтр для удаления сообщений из слишком активных ответчико
* [ ] добавить фильтр по полу для аккаунтов
* [ ] добавить фильтр по tag для диалогов и групп**ы**
* [ ] добавить мониторинг сцены, выполнилась ли сцена
* [ ] сделать в телеграм юзер импорт выбирать свободный прокси, если есть, загрузка файлов происходит всех трех файлов в модель
* [X] проверка вхождения в паблик, требуется ли
* [X] Оотправить юзеров всех в чат
* [X] проверка отправки сообщения по username
* [ ] покупка 50 аккаунтов
* [ ] покупка 50 прокси
* [X] расписать диалоги 10 штук для начал
* [X] проверить новый ипорт
* [X] проверка прокси
* [X] проверить тест юзера
* [X] поставить паузу для отправки сообщений**s**ыя
* [X] Сделать парсинг диалогов с чата
* [X] Алгоритм расбивающий чат на диалоги ( 1 диалог должен проходит в 12 часов, диалог максимум содержит 20 человек)
* [X] Добавить проверку всех пользователей в чате в метод is_ready в диало
* [X] добавить время в сообщения
* [X] добавить теги в диалоги
* [X] добавить select 2
* [X] Расписать модел планирования диалогов и как должны работать диалоги по времени
* [X] при создании юзера нужно чтобы был чек и получение всей информации о юзере, пол и имя
* [X] Добавит фильтры для Scenes чтобы можно было понимать сколько и как юзеры в каких чатах пишут сообщения
* [X] Разобраться со временем создоваемых сообщений из чатов
* [X] разобраться с созданием сцены и отправки ее в Переодическую таску
* [X] добавить проверку что все юзеры в чате
* [X] Добавит фильтры в telegramGroupMessages**s**
* [X] Проверить почему ломается создание переодической таски
