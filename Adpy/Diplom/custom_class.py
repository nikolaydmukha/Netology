import time
import requests
import csv
import datetime
import os
from tqdm import tqdm
from constants import ACCESS_TOKEN, REQUEST_URL, CSV_FILE, SEX, RELATION
from functions import retry_on_error

# Класс для пользователя VK, пару которому ищем
class VKUser:
    def __init__(self, user_id):
        self.user_id = user_id
        self.account_id = None
        self.params = {
            'access_token': ACCESS_TOKEN,
            'v': '5.95',
            'user_ids': self.user_id,
        }

    @retry_on_error
    def send_request(self, method, params):
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        return data

    # Поиск информации о пользователе, для которого будем предлагать варианты знакомства
    def lovefinder_info(self):
        method = 'users.get'
        self.params['fields'] = 'bdate, interests, personal, relation, sex, city, country, interests, education,' \
                                'music, movies, tv, books'
        data = self.send_request(method, self.params)
        name = {}
        if 'error' not in data:
            if 'deactivated' not in data['response'][0].keys():
                self.account_id = data['response'][0]['id']  # цифровой id пользователя
                name['friends_list'] = self.get_friends_list(self.account_id)
                name['fullname'] = " ".join((data['response'][0]['first_name'], data['response'][0]['last_name']))
                name['id'] = data['response'][0]['id']
                fields = ['music', 'university_name', 'interests', 'books', 'movies', 'personal', 'city',
                          'country', 'bdate', 'sex', 'relation']
                for param in fields:
                    if param in ['city', 'country']:
                        name[param] = {}
                        if data['response'][0][param]['title']:
                            name[param]['title'] = data['response'][0][param]['title']
                            name[param]['id'] = data['response'][0][param]['id']
                        else:
                            name[param]['title'] = ''
                            name[param]['id'] = ''
                    elif param == 'bdate':
                        if 'bdate' in data['response'][0].keys():
                            name['bdate'] = data['response'][0]['bdate']
                            birth = data['response'][0]['bdate'].split(".")
                            date_now = datetime.datetime.now()
                            date_birth = datetime.datetime(int(birth[2]), int(birth[1]), int(birth[0]))
                            name['age'] = (date_now - date_birth).days // 365
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
        method = 'database.getCountries'
        self.params['need_all'] = 0
        with open(os.path.abspath(CSV_FILE), encoding='utf-8') as csvfile:
            data = csv.reader(csvfile)
            short_name = {}
            for row in data:
                short_name[row[0].strip().lower()] = row[1].strip()
        while True:
            try:
                country_name = input("Введите страну поиска:").lower().strip()
                if short_name[country_name]:
                    self.params['code'] = short_name[country_name]
            except KeyError:
                print("А-яй, такой страны нет. Повторите ввод.")
                continue
            else:
                break
        data = self.send_request(method, self.params)
        return data['response']['items'][0]['id']  # Возвратим id страны по базе ВК

    # Выбор региона города
    def get_regions(self, country_id):
        method = 'database.getRegions'
        self.params['country_id'] = country_id
        self.params['count'] = 1000
        data = self.send_request(method, self.params)
        dict_of_region = {}
        print("\nВыберите регион из списка:")
        for row in data['response']['items']:
            dict_of_region[row['title'].lower()] = row['id']
            print(row['title'])
        while True:
            try:
                region_name = input("Введите регион поиска из списка выше:").lower().strip()
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
        method = 'database.getCities'
        self.params['country_id'] = self.get_country()
        region_id = self.get_regions(self.params['country_id'])
        self.params['region_id'] = region_id[0]
        self.params['count'] = 1000
        data = self.send_request(method, self.params)
        for row in data['response']['items']:
            print(row['title'])
        dict_of_cities = {}
        for row in data['response']['items']:
            dict_of_cities[row['title'].lower()] = row['id']
        while True:
            try:
                city_name = input("Введите город из списка выше:").lower().strip()
                if city_name == 'москва':
                    return [1, city_name, 1]
                elif city_name == 'санкт-петербург':
                    return [2, city_name, 1]
                else:
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
        method = 'groups.get'
        self.params['count'] = 1000
        self.params['user_id'] = account_id
        # response = requests.get(REQUEST_URL + method, self.params)
        # data = response.json()
        data = self.send_request(method, self.params)
        if 'error' not in data:
            return data['response']['items']

    # Поиск списка друзей
    def get_friends_list(self, account_id):
        method = "friends.get"
        self.params["count"] = 1000
        self.params["user_id"] = account_id
        self.params['fields'] = ''
        data = self.send_request(method, self.params)
        if 'error' not in data:
            return data['response']['items']
        else:
            return None

    # Поиск подходящих вариантов для знакомства
    def users_search(self, search_params):
        """
            Параметры:
                search_params[0] - sex
                search_params[1] - age_range
                search_params[2] - территория поиска:
                [0] - id города, [1] - название города, [2] - id страны
                отбрасываем тех, у кого указано в семейном поожении, что они в отношениях
        """
        method = 'users.search'
        self.params['sex'] = search_params[0]
        self.params['country'] = search_params[2][2]
        self.params['city'] = search_params[2][0]
        self.params['age_from'] = search_params[1][0]
        self.params['age_to'] = search_params[1][1]
        self.params['fields'] = 'relation, books, interests, music, movies, personal, bdate'
        data = self.send_request(method, self.params)
        finded_users = {}
        for item in tqdm(data['response']['items']):
            # Сразу отсекаем тех, кто уже имеет пару. При этом считаем, что если пользователь не захотел вообще
            # указывать семейное положение, то по дефолту выставляем 9 - не указано и добавляем в выборку
            if 'relation' not in item:
                item['relation'] = 0
            if item['relation'] in [1, 6, 0]:
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
                                birth = item[param].split(".")
                                date_now = datetime.datetime.now()
                                date_birth = datetime.datetime(int(birth[2]), int(birth[1]), int(birth[0]))
                                finded_users[fullname]['age'] = (date_now - date_birth).days // 365
                            else:
                                finded_users[fullname]['age'] = ''
                        finded_users[fullname][param] = item[param]
                    else:
                        finded_users[fullname][param] = ''
                        finded_users[fullname]['age'] = ''
                finded_users[fullname]['groups_list'] = self.get_groups(finded_users[fullname]['id'])
                finded_users[fullname]['friends_list'] = self.get_friends_list(finded_users[fullname]['id'])
                finded_users[fullname]['photos_url'] = self.get_photos()
        return finded_users

    # Поиск фотографий аватара
    def get_photos(self):
        method = "photos.get"
        self.params["count"] = 100
        self.params["album_id"] = 'profile'
        self.params['extended'] = 1
        data = self.send_request(method, self.params)
        dict_photos = []
        if 'error' not in data:
            for photo in data['response']['items']:
                finded_photos = {}
                # photo_id = photo['id']
                likes = photo['likes']['count']
                finded_photos['likes'] = likes
                finded_photos['url'] = ''
                # Полагаем, что самый маленький размер есть всегда. А вот фото в среднем или крупном размере - нет
                # Поэтому сразу сохраним маленькую фотографию, но если встретим среднюю, то сохраним её
                for size in photo['sizes']:
                    if (size['type'] == 's') & (not finded_photos['url']):
                        finded_photos['url'] = size['url']
                    elif size['type'] == 'r':
                        finded_photos['url'] = size['url']
                dict_photos.append(finded_photos)
            sorted_dict_photos = sorted(dict_photos, key=lambda k: k['likes'])
            urls = []
            for link in sorted_dict_photos[-3:]:
                urls.append(link['url'])
            self.params['extended'] = None
            return urls
        else:
            self.params['extended'] = None
            return None
