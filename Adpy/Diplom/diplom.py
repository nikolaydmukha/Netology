import time
import requests
import sys
import json
import os
#import psycopg2
from constants import ACCESS_TOKEN, REQUEST_URL


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
        print(data)
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


def start_programm():
    user = VKUser(sys.argv[1])
    print(sys.argv[1])
    if len(user.get_name()) != 2:
        print('Привет! Сейчас мы искать пару пользователю с идентификатором соцсети VK "{}"'.format(sys.argv[1]))
        print(f'Ты ввёл пользователя: {user.get_name()[0]}\nПол пользователя: \nВозраст пользователя: ')
        print(f"Программа выполнена. Данные записаны в файл {os.path.join(os.path.abspath('files'))}\diplom.json")
    else:
        sys.exit("Введённый пользователь заблокирован или удалён. Программа завершает свою работу!")


if __name__ == "__main__":
    start_programm()