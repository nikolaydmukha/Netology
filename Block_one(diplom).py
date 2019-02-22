import time
import requests
import sys
import progressbar
import json
import os
from pprint import pprint
from urllib.parse import urlencode


REQUEST_URL = "https://api.vk.com/method/"
ACCESS_TOKEN = "ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae"


# Функция получения ссылки для access_token
def get_token():
    AUTH_URL = "https://oauth.vk.com/authorize"
    V = "5.92"
    APP_ID = 6853214
    params = {
        'client_id': APP_ID,
        'display': 'page',
        'response_type': 'token',
        'v': '5.92',
        'scope': 'friends, users, groups',
    }
    print("?".join((AUTH_URL, urlencode(params))))


class VKUser:
    def __init__(self, user_id):
        self.user_id = user_id
        self.account_id = None
        self.params = {
            'access_token': ACCESS_TOKEN,
            'v': '5.92',
            'user_ids': self.user_id,
        }

    def get_name(self):
        time.sleep(1) #сделал задержку в 1 сек, т.к. получал ошибку от ВК, что слишком много запросов в сек
        method = "users.get"
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        self.account_id = data['response'][0]['id'] # цифровой id пользователя
        name = " ".join((data['response'][0]['first_name'], data['response'][0]['last_name']))
        return name

    def get_friends_list(self):
        time.sleep(1) #сделал задержку, т.к. получал ошибку от ВК, что слишком много запросов в сек
        method = "friends.get"
        self.params["count"] = 5000
        self.params["user_id"] = self.account_id
        self.params['fields'] = ''
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        return data['response']['items']

    def get_groups(self):
        time.sleep(1)  # сделал задержку, т.к. получал ошибку от ВК, что слишком много запросов в сек
        method = 'groups.get'
        self.params['count'] = 500
        self.params['user_id'] = self.account_id
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        return data['response']['items']

    def get_groups_by_id(self, list_groups):
        time.sleep(1)  # сделал задержку, т.к. получал ошибку от ВК, что слишком много запросов в сек
        method = 'groups.getById'
        self.params['group_ids'] = ','.join(map(str, list_groups))
        self.params['fields'] = 'members_count'
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        #print("222222222",data)
        names = ''
        to_file = []
        to_file_dict = {}
        for list_dict in data['response']:
            names += list_dict['name'] + ', '
            to_file_dict['name'] = list_dict['name']
            to_file_dict['gid'] = list_dict['id']
            to_file_dict['members_count'] = list_dict['members_count']
            to_file.append(to_file_dict)
            to_file_dict = {}
        #return names.rstrip(', ')
        return to_file


# Функция поиска участников группы
def get_group_member(g_id):
        params = {
            'access_token': ACCESS_TOKEN,
            'v': '5.92',
            'group_id': group_id
        }
        time.sleep(1)  # сделал задержку, т.к. получал ошибку от ВК, что слишком много запросов в сек
        method = 'groups.getMembers'
        response = requests.get(REQUEST_URL + method, params)
        data = response.json()
        if 'error' not in data.keys():
            return data['response']['items']


# Функция записи в файл
def write_json(dump):
    with open(os.path.join(os.path.abspath('files'), 'diplom.json'), 'w', encoding='utf-8') as f:
        json.dump(dump, f, ensure_ascii=False, indent=4)

#print(get_token())
User = VKUser(sys.argv[1])
print('Привет! Сейчас мы выведем список групп, в которых не состоит никто из друзей введённого тобой человека '
      'с идентификатором соцсети VK "{}"'.format(sys.argv[1]))
print(f'Ты ввёл пользователя: {User.get_name()}\nЧисло друзей пользователя {len(User.get_friends_list())}.')
#      f'\nПользователь состоит в таких группах: {User.get_groups_by_id(User.get_groups())}')
print('Получаем списки участников каждой группы, в которой состоит искомый пользователь ...')
# Список всех друзей
# Список всех групп
# Список участников каждой группы groups.getMembers
pbar = progressbar.ProgressBar()
groups_members = {}
for group_id in pbar(User.get_groups()):
    groups_members[group_id] = get_group_member(group_id) # словарь, в котором ключ - id группы, а значение - список участникв(id пользователей)
pbar = progressbar.ProgressBar()
print('Получаем группы, в которых нет ни одного друга искомого пользователя ...')
unique = []
for key, value in pbar(groups_members.items()):
    if value:
        check = set(value) & set(User.get_friends_list())
        if not check:
            unique.append(key)
unique_name = User.get_groups_by_id(unique)
#print(f"Группы, где нет друзей: {unique_name}")
write_json(unique_name)
print(f"Программа выполнена. Данные записаны в файл {os.path.join(os.path.abspath('files'))}\diplom.json")