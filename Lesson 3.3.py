# Вам предстоит решить задачу поиска общих друзей у пользователей VK.
#
# Ссылка на документацию VK/dev.

# Задача №1
# Пользователя нужно описать с помощью класса и реализовать метод поиска общих друзей, используя API VK.
#
# Задача №2
# Поиск общих друзей должен происходить с помощью оператора &, т.е. user1 & user2 должен выдать список общих друзей пользователей user1 и user2, в этом списке должны быть экземпляры классов.
#
# Задача №3
# Вывод print(user) должен выводить ссылку на профиль пользователя в сети VK
import time
import requests
from pprint import pprint
from urllib.parse import urlencode


REQUEST_URL = "https://api.vk.com/method/"
ACCESS_TOKEN = "b32e666359b816b4af0a75ae33b79856efc7b0a15bf17ff346820f0a50d3ea8296c1fd3e05b1da7f6d975"


class VKUser:
    def __init__(self, user_id):
        self.user_id = user_id
        self.params = {
            "access_token": ACCESS_TOKEN,
            "v": "5.92",
            "user_ids": self.user_id,
        }

    def get_name(self):
        time.sleep(1) #сделал задержку в 1 сек, т.к. получал ошибку от ВК, что слишком много запросов в сек
        method = "users.get"
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        #print(data)
        self.account_id = data['response'][0]['id'] # цифровой id пользователя
        name = " ".join((data['response'][0]['first_name'], data['response'][0]['last_name']))
        # print(data)
        return name

    def get_friends_list(self):
        time.sleep(1) #сделал задержку в 1 сек, т.к. получал ошибку от ВК, что слишком много запросов в сек
        method = "friends.get"
        self.params["count"] = 5000
        self.params["user_id"] = self.account_id
        # print(self.params)
        response = requests.get(REQUEST_URL + method, self.params)
        data = response.json()
        return data['response']['items']

    def __and__(self, other):
        me = self.get_friends_list()
        friend = other.get_friends_list()
        set_me = set(me)
        set_friend = set(friend)
        common_friends = set_me & set_friend
        common_friends_dict = {}
        common_friends_list = []
        for friend in common_friends:
            common_friends_list.append(VKUser(friend))  # список бщих друзей(каждый - экземпляр класса VKUser)
            name = VKUser(friend).get_name()
            common_friends_dict[name] = {'id': friend, 'url': 'https://vk.com/id' + str(friend)}
        print("Найдено {} обших друзей".format(len(common_friends_list)))
        for item in common_friends_list:
            print("{} <-> cсылка на профиль: {}".format(item.get_name(), common_friends_dict[item.get_name()]['url']))


# def find_common_friends(list1, list2):
#     set_me = set(list1)
#     set_friend = set(list2)
#     common_friends = set_me & set_friend
#     common_friends_dict = {}
#     common_friends_list = []
#     for friend in common_friends:
#         common_friends_list.append(VKUser(friend)) #список бщих друзей(каждый - экземпляр класса VKUser)
#         name = VKUser(friend).get_name()
#         common_friends_dict[name] = {'id': friend, 'url': 'https://vk.com/id' + str(friend)}
#     print("Найдено {} обших друзей".format(len(common_friends_list)))
#     for item in common_friends_list:
#         print("{} <-> cсылка на профиль: {}".format(item.get_name(), common_friends_dict[item.get_name()]['url']))


# Функция получения ссылки для access_token
def get_token():
    AUTH_URL = "https://oauth.vk.com/authorize"
    V = "5.92"
    APP_ID = 6853214
    params = {
        "client_id": APP_ID,
        "display": "page",
        "response_type": "token",
        "v": "5.92",
        "scope": "friends, users",
    }
    print("?".join((AUTH_URL, urlencode(params))))

Me = VKUser("dmukha")
Friend = VKUser("jdmukha")
print('Список id друзей пользователя {}(всего друзей {}):\n{}'.format(Me.get_name(), len(Me.get_friends_list()),
                                                                      Me.get_friends_list()))
print('Список id друзей пользователя {}(всего друзей {}):\n{}'.format(Friend.get_name(), len(Friend.get_friends_list()),
                                                                      Friend.get_friends_list()))
#find_common_friends(Me.get_friends_list(), Friend.get_friends_list())
Me&Friend
