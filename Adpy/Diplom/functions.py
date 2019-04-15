import time
import requests
import json
import csv
import datetime
import os
from pprint import pprint
from constants import ACCESS_TOKEN, REQUEST_URL, CSV_FILE, SEX, RELATION, POLITICAL, PEOPLE_MAIN, LIFE_MAIN, SMOKING
from constants import ALCOHOL


class VKUser:
    def __init__(self, user_id):
        self.user_id = user_id
        self.account_id = None
        self.params = {
            'access_token': ACCESS_TOKEN,
            'v': '5.95',
            'user_ids': self.user_id,
        }

    # Поиск информации о пользователе, для которого будем предлагать варианты знакомства
    def lovefinder_info(self):
        time.sleep(1)
        method = 'users.get'
        self.params['fields'] = 'bdate, interests, personal, relation, sex, city, country, interests, education,' \
                                'music, movies, tv, books'
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        #pprint(data)
        name = {}
        if 'error' not in data.keys():
            if 'deactivated' not in data['response'][0].keys():
                self.account_id = data['response'][0]['id'] # цифровой id пользователя
                name['groups'] = self.get_groups(self.account_id)
                print(len(name['groups']))
                name['fullname'] = " ".join((data['response'][0]['first_name'], data['response'][0]['last_name']))
                if data['response'][0]['sex']:
                    name['sex'] = SEX[data['response'][0]['sex']]
                else:
                    name['sex'] = ''
                if data['response'][0]['relation']:
                    name['relation'] = RELATION[data['response'][0]['relation']]
                else:
                    name['relation'] = ''
                if data['response'][0]['music']:
                    name['music'] = data['response'][0]['music']
                else:
                    name['relation'] = ''
                if data['response'][0]['university_name']:
                    name['university_name'] = data['response'][0]['university_name']
                else:
                    name['university_name'] = ''
                if data['response'][0]['interests']:
                    name['interests'] = data['response'][0]['interests']
                else:
                    name['interests'] = ''
                if data['response'][0]['books']:
                    name['books'] = data['response'][0]['books']
                else:
                    name['books'] = ''
                if data['response'][0]['movies']:
                    name['movies'] = data['response'][0]['movies']
                else:
                    name['movies'] = ''
                if data['response'][0]['personal']:
                    name['personal'] = data['response'][0]['personal']
                else:
                    name['movies'] = ''
                if data['response'][0]['bdate']:
                    name['bdate'] = data['response'][0]['bdate']
                    name['age'] = datetime.datetime.now().year - int(data['response'][0]['bdate'][-4:])
                else:
                    name['bdate'] = ''
                    name['age'] = ''
                name['city'] = {}
                name['country'] = {}
                if data['response'][0]['city']['title']:
                    name['city']['title'] = data['response'][0]['city']['title']
                    name['city']['id'] = data['response'][0]['city']['id']
                else:
                    name['city']['title'] = ''
                    name['city']['id'] = ''
                if data['response'][0]['country']['title']:
                    name['country']['title'] = data['response'][0]['country']['title']
                    name['country']['id'] = data['response'][0]['country']['id']
                else:
                    name['country']['title'] = ''
                    name['country']['id'] = ''
                return name
            else:
                self.account_id = data['response'][0]['id']  # цифровой id пользователя
                name['fullname'] = ' '.join((data['response'][0]['first_name'], data['response'][0]['last_name']))
                name['reason'] = "deleted"
                return name
        else:
            name['error'] = data['error']['error_msg']
            return name

    # Поиск идентификатора страны по имени
    def get_country(self):
        time.sleep(1)
        with open(os.path.abspath(CSV_FILE), encoding='utf-8') as csvfile:
            data = csv.reader(csvfile)
            short_name = {}
            for row in data:
                short_name[row[0].strip().lower()] = row[1].strip()
        method = 'database.getCountries'
        while True:
            try:
                country_name = input("Введите страну поиска:").lower()
                if short_name[country_name]:
                    self.params['code'] = short_name[country_name]
            except KeyError:
                print("А-яй, такой страны нет. Повторите ввод.")
                continue
            else:
                break
        self.params['need_all'] = 0
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        # Возвратим id страны по базе ВК
        return data['response']['items'][0]['id']

    # Выбор региона города
    def get_regions(self, country_id):
        time.sleep(1)
        method = 'database.getRegions'
        response = requests.get(REQUEST_URL + method, self.params)
        self.params['country_id'] = country_id
        self.params['count'] = 1000
        data = response.json()
        dict_of_region = {}
        print("\nВыберите регион из списка:")
        for row in data['response']['items']:
            dict_of_region[row['title'].lower()] = row['id']
            print(row['title'])
        while True:
            try:
                region_name = input("Введите регион поиска:").lower()
                if dict_of_region[region_name]:
                    pass
            except KeyError:
                print("А-яй, неппавильно ввели регион. Повторите ввод.")
                continue
            else:
                break
        return [dict_of_region[region_name], region_name, country_id]

    # Поиск идентификатора города по стране и имени города
    def get_city(self):
        time.sleep(1)
        method = 'database.getCities'
        self.params['country_id'] = self.get_country()
        region_id = self.get_regions(self.params['country_id'])
        self.params['region_id'] = region_id[0]
        self.params['count'] = 1000
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        #print(data)
        for row in data['response']['items']:
            pprint(row['title'])
        dict_of_cities = {}
        print("\nВыберите город из списка:")
        for row in data['response']['items']:
            dict_of_cities[row['title'].lower()] = row['id']
            print(row['title'])
        while True:
            try:
                city_name = input("Введите регион поиска:").lower()
                if dict_of_cities[city_name]:
                    pass
            except KeyError:
                print("А-яй, неппавильно ввели регион. Повторите ввод.")
                continue
            else:
                break
        return [dict_of_cities[city_name], city_name, region_id[2]]

    # Поиск групп
    def get_groups(self, account_id):
        print("start:  ",account_id)
        time.sleep(1)
        method = 'groups.get'
        self.params['count'] = 500
        self.params['user_id'] = account_id
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        if 'error' not in data.keys():
            return data['response']['items']

    # Поиск подходящих вариантов для знакомства
    def users_search(self, search_params):
        """
        search_params[0] - sex
        search_params[1] - age_range
        search_params[2] - территория поиска
                       [0] - id города, [1] - название города, [2] - id страны
        """
        self.params['sex'] = search_params[0]
        self.params['country'] = search_params[2][2]
        self.params['city'] = search_params[2][0]
        self.params['age_from'] = search_params[1][0]
        self.params['age_to'] = search_params[1][1]
        print((self.params))
        time.sleep(1)
        method = 'users.search'
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        #pprint(data)
        finded_users = {}
        for item in data['response']['items']:
            # сразу отсекаем тех, кто имеет пару. При этом считаем, что если пользователь не захотел вообще
            # указывать семейное положение, то считаем по дефолту 9 - не указано
            if 'relation' not in item.keys():
                item['relation'] = 0
            #if 'relation' in item.keys():
            if item['relation'] not in [2, 3, 4, 5, 7, 8]:
                fullname = item['first_name'] + ' ' + item['last_name']
                finded_users[fullname] = {}
                finded_users[fullname]['relation'] = item['relation']
                finded_users[fullname]['id'] = item['id']
                if 'books' in item.keys():
                    finded_users[fullname]['books'] = item['books']
                else:
                    finded_users[fullname]['books'] = ''
                if 'interests' in item.keys():
                    finded_users[fullname]['interests'] = item['interests']
                else:
                    finded_users[fullname]['interests'] = ''
                if 'movies' in item.keys():
                    finded_users[fullname]['movies'] = item['movies']
                else:
                    finded_users[fullname]['movies'] = ''
                if 'music' in item.keys():
                    finded_users[fullname]['music'] = item['music']
                else:
                    finded_users[fullname]['music'] = ''
                if 'personal' in item.keys():
                    finded_users[fullname]['personal'] = item['personal']
                else:
                    finded_users[fullname]['personal'] = ''
            finded_users[fullname]['groups'] = self.get_groups(finded_users[fullname]['id'])
            pprint(finded_users)


# Установка параметров поиска: пол
def set_search_gender():
    while True:
        try:
            sex = int(input("Укажите пол:\n    1 - женский, 2 - мужской"))
            if (sex != 1) & (sex!= 2):
                print("Вы выбрали не один из предложенных вариантов. Повторите выбор.")
                continue
        except ValueError:
            print("А-яй, вы ввели не число. Повторите ввод.")
            continue
        else:
            break
    return sex


# Установка параметров поиска: диапазон возраста
def set_search_age():
    age = []
    while True:
        try:
            print('Возраст от: ')
            age_from = int(input())
            if age_from < 0 or age_from == 0:
                print("Возраст не может быть отрицательным или равным 0.")
                continue
        except ValueError:
            print("А-яй, вы ввели не число. Повторите ввод.")
            continue
        else:
            age.append(age_from)
            while True:
                try:
                    print('Возраст до: ')
                    age_to = int(input())
                    if age_to <= age_from:
                        print("Возраст 'до' не может быть больше возраста 'от'.")
                        continue
                except ValueError:
                    print("А-яй, вы ввели не число. Повторите ввод.")
                    continue
                else:
                    age.append(age_to)
                    break
            break
    return age