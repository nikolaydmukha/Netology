import csv
import re
import os
import datetime
from pymongo import MongoClient


def clear_db(lesson_db):
    artists_collection = lesson_db['artists']
    artists_collection.drop()


def read_data(csv_file, lesson_db):
    """
    Загрузить данные в бд из CSV-файла
    """
    # создание коллекции
    artists_collection = lesson_db['artists']
    #artists_collection.drop()
    with open(os.path.abspath(csv_file), encoding='utf8') as csvfile:
        # прочитать файл с данными и записать в коллекцию
        reader = csv.DictReader(csvfile)
        # список словарея для вставки в коллекцию Mongo
        insert_to_mongo = []
        for item in reader:
            day, month = item['Дата'].split('.')
            artist_dict = {'Исполнитель': item['Исполнитель'], 'Цена': int(item['Цена']), 'Место': item['Место'],
                           'Дата': datetime.datetime(2019, int(month), int(day))}
            insert_to_mongo.append(artist_dict)
        # Записываем данные в коллекцию Mongo
        artists_collection.insert_many(insert_to_mongo)


def find_cheapest(lesson_db):
    """
    Найти самые дешевые билеты
    Документация: https://docs.mongodb.com/manual/reference/operator/aggregation/sort/
    """
    # создание коллекции
    artists_collection = lesson_db['artists']
    print("ТОП-3 самых дешёвых билетов:")
    for user in enumerate(artists_collection.find().sort('Цена', 1)[:3], start=1):
        print(f"{user[0]}. Исполнитель: {user[1]['Исполнитель']} | Место проведения: {user[1]['Место']} | Цена: {user[1]['Цена']}")


def sort_by_date(lesson_db):
    """
    Сортировка по дате концерта
    """
    # создание коллекции
    artists_collection = lesson_db['artists']
    print("Сортировка по дате:")
    for user in artists_collection.find().sort('Дата', 1):
        print(f"Дата: {user['Дата']} Исполнитель: {user['Исполнитель']} | Место проведения: {user['Место']} | Цена: {user['Цена']}")


def find_by_date(day_start, month_start, day_end, month_end, lesson_db):
    """
    Найти концерты в указанный период.
    Функция примнимает параметры: день начала, месяц начала, день конца и месяц конца поиска
    """
    # создание коллекции
    artists_collection = lesson_db['artists']
    start = datetime.datetime(2019,month_start, day_start)
    end = datetime.datetime(2019,month_end, day_end)
    print(f"Найденный концерты в период с {day_start}.{month_start} по {day_end}.{month_end}")
    for user in enumerate(artists_collection.find({'Дата': {'$gte': start, '$lte': end}}).sort('Дата', 1), start=1):
        print(f"{user[0]}. Дата: {user[1]['Дата']} Исполнитель: {user[1]['Исполнитель']} | Место проведения: {user[1]['Место']} | Цена: {user[1]['Цена']}")


def find_by_name(name, lesson_db):
    """
    Найти билеты по имени исполнителя (в том числе – по подстроке),
    и выведите их по возрастанию цены.
    """
    # создание коллекции
    artists_collection = lesson_db['artists']
    #expression = "(?i)" + name
    expression = name
    regex = re.compile(rf'\w*{expression}\w*')
    result = artists_collection.find({'Исполнитель': name}).sort('Цена', 1)
    find = False
    print("По вашему запросу найдены концерты: ")
    for item in enumerate(result, start=1):
        print(f"{item[0]}. Исполнитель: {item[1]['Исполнитель']} | Место проведения: {item[1]['Место']}"
              f" | Цена: {item[1]['Цена']}")
        find = True
    if not find:
        print("...точных совпадений не найдено, но можете обратить внимание на эти концерты:")
        result = artists_collection.find({'Исполнитель': regex}).sort('Цена', 1)
        for item in enumerate(result,start=1):
            print(f"{item[0]}. Исполнитель: {item[1]['Исполнитель']} | Место проведения: {item[1]['Место']}"
                  f" | Цена: {item[1]['Цена']}")


if __name__ == '__main__':
    # коннект к MongoDB
    client = MongoClient()
    # создание БД
    lesson_db = client['MongoLesson']
    # очистить базу, если необходимо
    clear_db(lesson_db)
    # читаем csv в БД
    read_data('artists.csv', lesson_db)
    # поиск ТОП-3 самых дешёвых билетов
    find_cheapest(lesson_db)
    # поиск артиста по имени или подстроке
    find_by_name('`', lesson_db)
    # вывод отсортированных по дате событий
    sort_by_date(lesson_db)
    find_by_date(1, 2, 28, 2, lesson_db)
