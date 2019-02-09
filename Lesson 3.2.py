# Задача №1
# Необходимо чтобы функцию переводчика принимала следующие параметры:
#
# Путь к файлу с текстом;
# Путь к файлу с результатом;
# Язык с которого перевести;
# Язык на который перевести (по-умолчанию русский).
# У вас есть 3 файла (DE.txt, ES.txt, FR.txt) с новостями на 3 языках: французском, испанском, немецком. Функция должна
# взять каждый файл с текстом, перевести его на русский и сохранить результат в новом файле.


import requests
from pprint import pprint

API_KEY = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


# Функция перевода текста, читаемого из файла. Результат перевода записывается в файл
def translate_it(path_file_from, path_file_to, from_lang, to_lang="ru"):
    # Я читаю файл построчно, чтобы получить текст в типе str(а не список) для передачи переводчику
    with open(path_file_from, encoding="utf-8") as file:
        text = ""
        for line in file:
            text += line
    params = {
        'key': API_KEY,
        'text': text,
        'lang': '{}-{}'.format(from_lang, to_lang),
    }
    response = requests.get(URL, params=params)
    json_ = response.json()
    # Запись в файл: переводчик возвращает текст в виде списка. В файл надо записать каждый элемент списка
    with open(path_file_to, "w", encoding='utf-8') as f:
        for member in json_["text"]:
            f.write(member)


# Функция подготавливает необходимые для работы функции перевода данные
def make_translate():
    file_dir = 'D:\Python\\Netology\\Netology\\files\\'
    dict_files = {
        "DE.txt": "fromDE.txt",
        "ES.txt": "fromES.txt",
        "FR.txt": "fromFR.txt",
    }
    for fr, to in dict_files.items():
        path_file_from = file_dir + fr
        path_file_to = file_dir + to
        from_lang = fr.split(".")
        translate_it(path_file_from, path_file_to, from_lang[0].lower())


make_translate()

