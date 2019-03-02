# Написать класс итератора, который по каждой стране из файла countries.json ищет страницу из википедии.
# Записывает в файл пару: страна – ссылка.
#
# Написать генератор, который принимает путь к файлу. При каждой итерации возвращает md5 хеш каждой строки файла
import os
import json


class Wiki:
    def __init__(self, start, end):
        self.start, self.end = start-1, end

    def __iter__(self):
        return self

    def __next__(self):
        self.start += 1
        if self.start == self.end:
            raise StopIteration
        return self.start


if __name__ == "__main__":
    with open(os.path.abspath('countries.json'), 'r', encoding='koi8-r') as js:
        data = json.load(js)
        print(data)