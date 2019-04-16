import os
import sys
from functions import VKUser, set_search_gender, set_search_age
from pprint import pprint


def start_programm():
    ##user = VKUser(sys.argv[1])
    ##print(sys.argv[1])
    #username = "155686070"
    username = "29827545"
    user = VKUser(username)
    lovefinder_data = user.lovefinder_info()
    if 'error' not in lovefinder_data.keys():
        if 'reason' not in lovefinder_data.keys():
            ##print(f'Привет! Сейчас мы искать пару пользователю с идентификатором соцсети VK "{sys.argv[1]}"')
            print(f'Привет! Сейчас мы будем искать пару пользователю с идентификатором соцсети VK "{username}".\n'
                  f'Короткая справка о пользователе (может помочь при составлении запроса на поиск пары):')
            print(f'Полное имя: {lovefinder_data["fullname"]}\nПол: {lovefinder_data["sex"]}'
                  f'  \nДата рождения: {lovefinder_data["bdate"]} (возраст {lovefinder_data["age"]})\n'
                  f'Страна и город проживания: {lovefinder_data["country"]["title"]} ({lovefinder_data["city"]["title"]})'
                  f'\nВысшее образование: {lovefinder_data["university_name"]}\n')
            print('Давайте сформируем параметры поиска.')
            sex = set_search_gender()
            age_range = set_search_age()
            city = user.get_city() #city[0] - id города, city[1] - название города, city[3] - id страны
            print(f"Производим поиск людей по условиям: пол: {sex[1]}, возраст: от {age_range[0]} до {age_range[1]}, город: {city[1]}")
            search_params = [sex[0], age_range,city]
            filtered_users = user.users_search(search_params)
            pprint(filtered_users)
            print(f"Найдено {len(filtered_users)} человек в первой выборке. Подберём людей, исходя из более точных "
                  f"условий.")
            pprint(lovefinder_data)
            print(f"Программа выполнена. Данные записаны в файл {os.path.join(os.path.abspath('files'))}\diplom.json")
        else:
            sys.exit(f"Что-то пошло не так :( пользователь удалил свою страницу.")
    else:
        sys.exit(f"Что-то пошло не так :( {lovefinder_data['error']}")


if __name__ == "__main__":
    start_programm()
