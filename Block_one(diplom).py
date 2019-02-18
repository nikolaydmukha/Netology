import time
import requests
import sys
import progressbar
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
        print(self.account_id)
        name = " ".join((data['response'][0]['first_name'], data['response'][0]['last_name']))
        return name

    def get_friends_list(self):
        time.sleep(1) #сделал задержку, т.к. получал ошибку от ВК, что слишком много запросов в сек
        method = "friends.get"
        self.params["count"] = 5000
        self.params["user_id"] = self.account_id
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        return data['response']['items']

    def get_groups(self):
        time.sleep(1)  # сделал задержку, т.к. получал ошибку от ВК, что слишком много запросов в сек
        method = 'groups.get'
        self.params['count'] = 500
        self.params['user_id'] = self.account_id
        #print(self.params)
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        #print(data)
        return data['response']['items']

    def get_groups_by_id(self, list_groups):
        time.sleep(1)  # сделал задержку, т.к. получал ошибку от ВК, что слишком много запросов в сек
        method = 'groups.getById'
        print("ПОЛУЧАЕМ ИМЕНЯ ГРУПП", list_groups)
        self.params['group_ids'] = ','.join(map(str, list_groups))
        #print(self.params['group_ids'])
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        names = ''
        for list_dict in data['response']:
            names += list_dict['name'] + ', '
        return names.rstrip(', ')


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
            print(data.keys())
            return data['response']['items']


#print(get_token())
User = VKUser(sys.argv[1])
print('Привет! Сейчас мы выведем список групп, в которых не состоит никто из друзей введённого тобой человека '
      'с идентификатором соцсети VK "{}"'.format(sys.argv[1]))
print(f'Ты ввёл пользователя: {User.get_name()}\nЧисло друзей пользователя {len(User.get_friends_list())}.'
      f'\nПользователь состоит в таких группах: {User.get_groups_by_id(User.get_groups())}')
print('Проверяем, состоят ли друзья в группах ввёдёного пользвателя..')
# Список всех друзей
# Список всех групп
# Список участников каждой группы groups.getMembers
groups_members = {}
for group_id in User.get_groups():
    groups_members[group_id] = get_group_member(group_id) # словарь, в котором ключ - id группы, а значение - список участникв(id пользователей)
pprint(groups_members.keys())
pbar = progressbar.ProgressBar()
unique = []
for key, value in pbar(groups_members.items()):
    if value:
        print("KEY", key)
        print("VALUE", value)
        check = set(value)&set(User.get_friends_list())
    #print("МОИ ДРУЗЬЯ", User.get_friends_list())
    #print("ДРУЗЬЯ ГРУППЫ", value)
    #print("Нашли общих друзей", check)
        if not check:
            unique.append(key)
unique_name = User.get_groups_by_id(unique)
print(unique_name)
print(f"Группы, где нет друзкй: {unique}")
    #print(key, value)
