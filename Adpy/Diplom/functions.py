import time
import requests
import json
import csv
import datetime
import os
from pprint import pprint
from tqdm import tqdm
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
        #time.sleep(1)
        method = 'users.get'
        self.params['fields'] = 'bdate, interests, personal, relation, sex, city, country, interests, education,' \
                                'music, movies, tv, books'
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        name = {}
        if 'error' not in data.keys():
            if 'deactivated' not in data['response'][0].keys():
                self.account_id = data['response'][0]['id'] # цифровой id пользователя
                name['groups'] = self.get_groups(self.account_id)
                name['friends_list'] = self.get_friends_list(self.account_id)
                name['fullname'] = " ".join((data['response'][0]['first_name'], data['response'][0]['last_name']))
                fields = ['music', 'university_name', 'interests', 'books', 'movies', 'personal', 'city',
                          'country', 'bdate', 'sex', 'relation']
                for param in fields:
                    ###print("PARAM", param)
                    if param in ['city', 'country']:
                        name[param] = {}
                        if data['response'][0][param]['title']:
                            name[param]['title'] = data['response'][0][param]['title']
                            name[param]['id'] = data['response'][0][param]['id']
                        else:
                            name[param]['title'] = ''
                            name[param]['id'] = ''
                    elif param == 'bdate':
                        if data['response'][0]['bdate']:
                            name['bdate'] = data['response'][0]['bdate']
                            name['age'] = datetime.datetime.now().year - int(data['response'][0]['bdate'][-4:])
                        else:
                            name['bdate'] = ''
                            name['age'] = ''
                    elif param == 'sex':
                        if data['response'][0][param]:
                            name[param] = SEX[data['response'][0][param]]
                        else:
                            name[param] = ''
                    elif param == 'relation':
                        if data['response'][0][param]:
                            name[param] = RELATION[data['response'][0][param]]
                        else:
                            name[param] = 0
                    else:
                        if data['response'][0][param]:
                            name[param] = data['response'][0][param]
                        else:
                            name[param] = ''
                name['groups_list'] = self.get_groups(data['response'][0]['id'])
                name['friends_list'] = self.get_friends_list(data['response'][0]['id'])
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
        #time.sleep(1)
        method = 'database.getCountries'
        self.params['need_all'] = 0
        with open(os.path.abspath(CSV_FILE), encoding='utf-8') as csvfile:
            data = csv.reader(csvfile)
            short_name = {}
            for row in data:
                short_name[row[0].strip().lower()] = row[1].strip()
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
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        #pprint(data)
        # Возвратим id страны по базе ВК
        return data['response']['items'][0]['id']

    # Выбор региона города
    def get_regions(self, country_id):
        #time.sleep(1)
        method = 'database.getRegions'
        self.params['country_id'] = country_id
        self.params['count'] = 1000
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        dict_of_region = {}
        print("\nВыберите регион из списка:")
        for row in data['response']['items']:
            dict_of_region[row['title'].lower()] = row['id']
            print(row['title'])
        while True:
            try:
                region_name = input("Введите регион поиска из списка выше:").lower()
                if dict_of_region[region_name]:
                    pass
            except KeyError:
                print("А-яй, неправильно ввели регион. Повторите ввод.")
                continue
            else:
                break
        return [dict_of_region[region_name], region_name, country_id]

    # Поиск идентификатора города по стране и имени города
    def get_city(self):
        #time.sleep(1)
        method = 'database.getCities'
        self.params['country_id'] = self.get_country()
        region_id = self.get_regions(self.params['country_id'])
        self.params['region_id'] = region_id[0]
        self.params['count'] = 1000
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        for row in data['response']['items']:
            print(row['title'])
        dict_of_cities = {}
        #print("\nВыберите город из списка:")
        for row in data['response']['items']:
            dict_of_cities[row['title'].lower()] = row['id']
            #print(row['title'])
        while True:
            try:
                city_name = input("Введите город из списка выше:").lower()
                if dict_of_cities[city_name]:
                    pass
            except KeyError:
                print("А-яй, неправильно ввели регион. Повторите ввод.")
                continue
            else:
                break
        return [dict_of_cities[city_name], city_name, region_id[2]]

    # Поиск групп
    def get_groups(self, account_id):
        time.sleep(1)
        method = 'groups.get'
        self.params['count'] = 1000
        self.params['user_id'] = account_id
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        if 'error' not in data.keys():
            return data['response']['items']

    # Поиск списка друзей
    def get_friends_list(self, account_id):
        time.sleep(1)
        method = "friends.get"
        self.params["count"] = 1000
        self.params["user_id"] = account_id
        self.params['fields'] = ''
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        if 'error' not in data.keys():
            return data['response']['items']
        else:
            return None

    # Поиск подходящих вариантов для знакомства
    def users_search(self, search_params):
        """
        search_params[0] - sex
        search_params[1] - age_range
        search_params[2] - территория поиска
                       [0] - id города, [1] - название города, [2] - id страны
        """
        time.sleep(1)
        method = 'users.search'
        self.params['sex'] = search_params[0]
        self.params['country'] = search_params[2][2]
        self.params['city'] = search_params[2][0]
        self.params['age_from'] = search_params[1][0]
        self.params['age_to'] = search_params[1][1]
        self.params['fields'] = 'relation, books, interests, music, movies, personal, bdate'
        #print(self.params)
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        #print(data)
        finded_users = {}
        for item in tqdm(data['response']['items']):
            # сразу отсекаем тех, кто имеет пару. При этом считаем, что если пользователь не захотел вообще
            # указывать семейное положение, то считаем по дефолту 9 - не указано
            if 'relation' not in item.keys():
                item['relation'] = 0
            if item['relation'] not in [2, 3, 4, 5, 7, 8]:
                fullname = item['first_name'] + ' ' + item['last_name']
                finded_users[fullname] = {}
                finded_users[fullname]['relation'] = item['relation']
                finded_users[fullname]['id'] = item['id']
                fields = ['music', 'interests', 'books', 'movies', 'sex', 'personal', 'bdate']
                for param in fields:
                    if param in item.keys():
                        if param == 'bdate':
                            if item[param]:
                                length_age = item[param].split('.')
                            else:
                                length_age = []
                            if len(length_age) == 3:
                                ###print("22222222222222222222222", item)
                                finded_users[fullname]['age'] = datetime.datetime.now().year - int(item[param][-4:])
                            else:
                                finded_users[fullname]['age'] = ''
                        ##finded_users[fullname][param] = item[param]
                        finded_users[fullname][param] = item[param]
                    else:
                        finded_users[fullname][param] = ''
                        finded_users[fullname]['age'] = ''
                # if 'books' in item.keys():
                #     finded_users[fullname]['books'] = item['books']
                # else:
                #     finded_users[fullname]['books'] = ''
                # if 'interests' in item.keys():
                #     finded_users[fullname]['interests'] = item['interests']
                # else:
                #     finded_users[fullname]['interests'] = ''
                # if 'movies' in item.keys():
                #     finded_users[fullname]['movies'] = item['movies']
                # else:
                #     finded_users[fullname]['movies'] = ''
                # if 'music' in item.keys():
                #     finded_users[fullname]['music'] = item['music']
                # else:
                #     finded_users[fullname]['music'] = ''
                # if 'personal' in item.keys():
                #     finded_users[fullname]['personal'] = item['personal']
                # else:
                #     finded_users[fullname]['personal'] = ''
                finded_users[fullname]['groups_list'] = self.get_groups(finded_users[fullname]['id'])
                finded_users[fullname]['friends_list'] = self.get_friends_list(finded_users[fullname]['id'])
        return finded_users


# Установка параметров поиска: пол
def set_search_gender():
    sex = []
    while True:
        try:
            print("Укажите пол:\n    1 - женский, 2 - мужской")
            sex_input = int(input())
            if (sex_input != 1) & (sex_input!= 2):
                print("Вы выбрали не один из предложенных вариантов. Повторите выбор.")
                continue
        except ValueError:
            print("А-яй, вы ввели не число. Повторите ввод.")
            continue
        else:
            break
    if sex_input == 1:
        sex = [sex_input, 'женский']
    else:
        sex = [sex_input, 'мужской']
    return sex


# Установка параметров поиска: диапазон возраста
def set_search_age():
    age = []
    while True:
        try:
            print('Возраст от: ')
            age_from = int(input())
            if age_from < 0 or age_from == 0 or len(str(age_from)) > 2:
                print("Возраст не может быть отрицательным, равным 0 и, вероятно, недвузначным.")
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
                    if age_to <= age_from or len(str(age_to)) > 2:
                        print("Возраст 'до' не может быть больше возраста 'от' и, вероятно, недвузначным..")
                        continue
                except ValueError:
                    print("А-яй, вы ввели не число. Повторите ввод.")
                    continue
                else:
                    age.append(age_to)
                    break
            break
    return age


# Поиск пары по критериям: общие друзья, общие группы, общие интересы, общая музыка
def compare_data(loverfinder, finded_users, filter_by, result):
    print("ФИЛЬТР ПО", filter_by)
    for key, data in finded_users.items():
        """
         Cовпадение по возрасту должны быть важнее общих групп. 
         Интересы по музыке важнее книг. 
         Наличие общих друзей важнее возраста.
        """
        if data[filter_by]:
            if filter_by == 'age':
                if finded_users[key][filter_by] == loverfinder[filter_by]:
                    finded_users[key][result] = loverfinder[filter_by]
                else:
                    finded_users[key][result] = ''
            else:
                if set(finded_users[key][filter_by]) & set(loverfinder[filter_by]):
                    finded_users[key][result] = len(set(finded_users[key][filter_by]) & set(loverfinder[filter_by]))
                else:
                    finded_users[key][result] = ''
        else:
            finded_users[key][result] = ''
            print("У пользователя закрытый профиль.")
    print("В ФУНКЦИИ!!!")
    pprint(finded_users)
    return data