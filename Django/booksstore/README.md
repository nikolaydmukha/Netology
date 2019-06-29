Прототип системы для библиотекаря
===
Данная система является прототипом для системы библиотекаря. 

**Основной функционал:**
1. Добавлены модели: 
    - _Книги_ - информация о книгах и о том, кому выдали
    - _Аторы_ - список авторов
    - _Читатели_ - список читателей
    - _Шкаф_ - номера шкафов, где находятся книги
    - _Полка_ - номера полок, , где находятся книги
    - _Место_ на полке - номера мест на полке, , где находятся книги
    - _Тэги_ - тэги
    - _Жанр_ - жанр книг
2. Добавление, изменение, удаление данных
3. Поиск книг по автору и по названию
4. Поиск читателей по имени
5. Возврат нескольких выбранных книг
6. Всё управление ведётся через стандартную админку(**не забудьте создать суперпользователя**)

**Stack программы:** _docker + Django 2.2 + Postgres_

Чтобы развернуть программу, нужно выполнить в docker команду:
_docker-compose up_