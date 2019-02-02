# Написать программу, которая будет выводить топ 10 самых часто встречающихся в новостях слов
# длиннее 6 символов для каждого файла.
#
# Не забываем про декомпозицию и организацию кода в функции. В решении домашнего задания вам
# могут помочь: split(), sort или sorted.
#
# Задача №1
# Написать программу для файла в формате json.
#
# Задача №2.
# Написать программу для файла в формате xml.


import json
import xml
import xml.etree.ElementTree as ET
from pprint import pprint


# Чтение данных из файла .json
def read_json():
    with open('D:\Python\\Netology\\Netology\\newsafr.json', encoding='utf-8') as js:
        js_data = json.load(js)
        articles = js_data['rss']['channel']['items']
        list_desc = []
        for new in articles:
            list_articles = new['description'].split(" ")
            for word in list_articles:
                list_desc.append(word)
    make_dict(list_desc, "json")


# Чтение данных из .xml
def read_xml():
    tree = ET.parse('D:\Python\\Netology\\Netology\\newsafr.xml')
    root = tree.getroot()
    descriptions = root.findall('channel/item/description')
    list_desc = []
    for desc in descriptions:
        for word in desc.text.split(" "):
            list_desc.append(word)
    make_dict(list_desc, "xml")


# Функция по созданию словаря со словами и их количеством их повторений
def make_dict(data, file_type):
    count_words = {}  # для записи числа повторений слов > 6 символов
    for word in data:
        if len(word) > 6:
            if word in count_words.keys():
                count_words[word] += 1
            else:
                count_words[word] = 1
    top_words(count_words, file_type)


# Сотировка и вывод 10 наиболее часто встречающихся слов
def top_words(count_words, file_type):
    count_words_k = count_words.keys()
    count_words_v = count_words.values()
    top = sorted(zip(count_words_v, count_words_k), reverse=True)
    print(f"\nТОП-10 наиболее популярных слов в новостях файла .{file_type}:")
    for value in top[0:10:1]:
        print(f"Слово '{value[1]}' встречается {value[0]} раз(а) в тексте новости!")


read_json()
read_xml()

