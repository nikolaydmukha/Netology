import time
import requests
import sys
import progressbar
import json
import os
from pprint import pprint


REQUEST_URL = "https://api.vk.com/method/"
ACCESS_TOKEN = "ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae"


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
        time.sleep(1)
        method = "users.get"
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        if 'deactivated' not in data['response'][0].keys():
                self.account_id = data['response'][0]['id'] # цифровой id пользователя
                name = " ".join((data['response'][0]['first_name'], data['response'][0]['last_name']))
                return name
        else:
            sys.exit("Введённый пользователь заблокирован или удалён. Программа завершает свою работу!")

    def get_friends_list(self):
        time.sleep(1)
        method = "friends.get"
        self.params["count"] = 5000
        self.params["user_id"] = self.account_id
        self.params['fields'] = ''
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        if 'error' not in data.keys():
            return data['response']['items']
        else:
            return None

    def get_groups(self):
        time.sleep(1)
        method = 'groups.get'
        self.params['count'] = 500
        self.params['user_id'] = self.account_id
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        return data['response']['items']

    def get_groups_by_id(self, list_groups):
        time.sleep(1)
        method = 'groups.getById'
        self.params['group_ids'] = ','.join(map(str, list_groups))
        self.params['fields'] = 'members_count'
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
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
        return to_file


# Функция поиска участников группы
def get_group_member(g_id):
        params = {
            'access_token': ACCESS_TOKEN,
            'v': '5.92',
            'group_id': g_id,
        }
        time.sleep(1)
        method = 'groups.getMembers'
        response = requests.get(REQUEST_URL + method, params)
        data = response.json()
        if 'error' not in data.keys():
            return data['response']['items']


# Прогресс-бар
def progress_bar(data):
    pbar = progressbar.ProgressBar()
    return pbar(data)


# Функция записи в файл
def write_json(dump):
    with open(os.path.join(os.path.abspath('files'), 'diplom.json'), 'w', encoding='utf-8') as f:
        json.dump(dump, f, ensure_ascii=False, indent=4)


User = VKUser(sys.argv[1])
print('Привет! Сейчас мы выведем список групп, в которых не состоит никто из друзей введённого тобой человека '
      'с идентификатором соцсети VK "{}"'.format(sys.argv[1]))
print(f'Ты ввёл пользователя: {User.get_name()}\nЧисло друзей пользователя {len(User.get_friends_list())}.')
print('Получаем списки участников каждой группы, в которой состоит искомый пользователь ...')
groups_members = {}
for group_id in progress_bar(User.get_groups()):
    groups_members[group_id] = get_group_member(group_id)
print('Получаем группы, в которых нет ни одного друга искомого пользователя ...')
unique = []
for key, value in progress_bar(groups_members.items()):
    if value:
        check = set(value) & set(User.get_friends_list())
        if not check:
            unique.append(key)
if not unique:
    write_json("Нет ни одной уникальной группы!")
else:
    unique_name = User.get_groups_by_id(unique)
    write_json(unique_name)
print(f"Программа выполнена. Данные записаны в файл {os.path.join(os.path.abspath('files'))}\diplom.json")
