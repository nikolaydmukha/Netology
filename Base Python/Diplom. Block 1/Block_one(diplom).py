import time
import requests
import sys
import json
import os
from tqdm import tqdm


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
        name = list()
        if 'deactivated' not in data['response'][0].keys():
            self.account_id = data['response'][0]['id'] # цифровой id пользователя
            name.append(" ".join((data['response'][0]['first_name'], data['response'][0]['last_name'])))
            return name
        else:
            self.account_id = data['response'][0]['id']  # цифровой id пользователя
            name.append(" ".join((data['response'][0]['first_name'], data['response'][0]['last_name'])))
            name.append("deleted")
            return name

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
        if 'error' not in data.keys():
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


# Функция записи в файл
def write_json(dump):
    with open(os.path.abspath('diplom.json'), 'w', encoding='utf-8') as f:
        json.dump(dump, f, ensure_ascii=False, indent=4)


def run_work():
    user = VKUser(sys.argv[1])
    if len(user.get_name()) != 2:
        print('Привет! Сейчас мы выведем список групп, в которых не состоит никто из друзей введённого тобой человека '
              'с идентификатором соцсети VK "{}"'.format(sys.argv[1]))
        print(f'Ты ввёл пользователя: {user.get_name()[0]}\nЧисло друзей пользователя {len(user.get_friends_list())}.')
        print('Получаем группы, в которых состоят друзья искомого пользователя...')
        group_list = []
        target = user.get_groups()
        for friend in user.get_friends_list():
            friend_id = VKUser(friend)
            print("Получаем список групп друга --->", friend_id.get_name()[0])
            if len(friend_id.get_name()) != 2:
                if friend_id.get_groups():
                    for group in tqdm(friend_id.get_groups()):
                        group_list.append(group)
                        time.sleep(0.1)
                else:
                    print("Пользователь удалён, заблокирован или включил настройки приватности своего аккаунта.")
            else:
                print("Пользователь удалён, заблокирован или включил настройки приватности своего аккаунта")
        unique = set(target) - set(group_list)
        if not unique:
            write_json("Нет ни одной уникальной группы!")
        else:
            unique_name = user.get_groups_by_id(unique)
            write_json(unique_name)
        print(f"Программа выполнена. Данные записаны в файл {os.path.join(os.path.abspath('files'))}\diplom.json")
    else:
        sys.exit("Введённый пользователь заблокирован или удалён. Программа завершает свою работу!")


if __name__ == "__main__":
    run_work()
