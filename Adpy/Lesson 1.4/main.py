# Написать класс итератора, который по каждой стране из файла countries.json ищет страницу из википедии.
# Записывает в файл пару: страна – ссылка.
#
# Написать генератор, который принимает путь к файлу. При каждой итерации возвращает md5 хеш каждой строки файла
import os
import json
import hashlib


class Wiki:
    def __init__(self, countries):
        self.countries = countries
        self.start = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.start += 1
        if self.start != len(self.countries):
            long = self.countries[self.start][0]
            short = self.countries[self.start][1]
            to_file = f'Ссылка Википедии страны "{long}" - https://{short.lower()}.wikipedia.org\n'
            with open(os.path.abspath('country-link'), 'a', encoding='utf-8') as f:
                f.write(to_file)
                return long
        else:
            raise StopIteration


def generator_md5(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
        for item in data:
            hash = hashlib.md5(item.encode('utf-8')).hexdigest()
            yield hash


if __name__ == "__main__":
    with open(os.path.abspath('countries.json'), 'r', encoding='utf-8') as js:
        name = []
        data = json.load(js)
        for item in data:
            long_short = [item['translations']['rus']['official'], item['cca2']]
            name.append(long_short)
    for wiki in Wiki(name):
        print(f"Записали для страны {wiki} соответствующую ссылку")
    print('Вывод md5 hash строки:\n')
    for md5 in generator_md5(os.path.abspath('country-link')):
        print(md5)
