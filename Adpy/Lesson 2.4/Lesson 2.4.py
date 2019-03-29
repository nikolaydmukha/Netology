import csv
import re
import os
import datetime
from pymongo import MongoClient


def read_data(csv_file, lesson_db):
    """
    Загрузить данные в бд из CSV-файла
    """
    # создание коллекции
    artists_collection = lesson_db['artists']
    artists_collection.drop()
    with open(os.path.abspath(csv_file), encoding='utf8') as csvfile:
        # прочитать файл с данными и записать в коллекцию
        reader = csv.DictReader(csvfile)
        # список словарея для вставки в коллекцию Mongo
        insert_to_mongo = []
        for item in reader:
            temp_date = item['Дата'].split('.')
            artist_dict = {'Исполнитель': item['Исполнитель'], 'Цена': int(item['Цена']), 'Место': item['Место'],
                           'Дата': datetime.datetime(2019, int(temp_date[1]), int(temp_date[0]))}
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
    k = 1
    print("ТОП-3 самых дешёвых билетов:")
    for user in artists_collection.find().sort('Цена', 1):
        if k <= 3:
            print(f"{k}. Исполнитель: {user['Исполнитель']} | Место проведения: {user['Место']} | Цена: {user['Цена']}")
            k += 1


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
    k = 1
    print(f"Найденный концерты в период с {day_start}.{month_start} по {day_end}.{month_end}")
    for user in artists_collection.find({'Дата': {'$gte': start, '$lte': end}}).sort('Дата', 1):
        print(f"{k}. Дата: {user['Дата']} Исполнитель: {user['Исполнитель']} | Место проведения: {user['Место']} | Цена: {user['Цена']}")
        k += 1


def find_by_name(name, lesson_db):
    """
    Найти билеты по имени исполнителя (в том числе – по подстроке),
    и выведите их по возрастанию цены.
    """
    # создание коллекции
    artists_collection = lesson_db['artists']
    expression = "(?i)" + name
    regex = re.compile(expression)
    result = artists_collection.find({'Исполнитель': name}).sort('Цена', 1)
    find = False
    print("По вашему запросу найдены концерты: ")
    k = 1
    for item in result:
        print(f"{k}. Исполнитель: {item['Исполнитель']} | Место проведения: {item['Место']} | Цена: {item['Цена']}")
        find = True
        k += 1
    if not find:
        result = artists_collection.find({'Исполнитель': regex}).sort('Цена', 1)
        for item in result:
            print(f"{k}. Исполнитель: {item['Исполнитель']} | Место проведения: {item['Место']} | Цена: {item['Цена']}")
            k += 1


if __name__ == '__main__':
    # коннект к MongoDB
    client = MongoClient()
    # создание БД
    lesson_db = client['MongoLesson']
    # читаем csv в БД
    read_data('artists.csv', lesson_db)
    # поиск ТОП-3 самых дешёвых билетов
    find_cheapest(lesson_db)
    # поиск артиста по имени или подстроке
    find_by_name('e', lesson_db)
    # вывод отсортированных по дате событий
    sort_by_date(lesson_db)
    find_by_date(1, 2, 28, 2, lesson_db)
