import os
import sys
from functions import VKUser, set_search_gender, set_search_age, compare_data
from pprint import pprint


def start_programm():
    ##user = VKUser(sys.argv[1])
    ##print(sys.argv[1])
    #username = "155686070"
    #username = "29827545"
    username = sys.argv[1]
    user = VKUser(username)
    lovefinder_data = user.lovefinder_info()
    if 'error' not in lovefinder_data.keys():
        if 'reason' not in lovefinder_data.keys():
            ##print(f'Привет! Сейчас мы искать пару пользователю с идентификатором соцсети VK "{sys.argv[1]}"')
            print(f'Привет! Сейчас мы будем искать пару пользователю с идентификатором соцсети VK "{username}".\n'
                  f'Короткая справка о пользователе (может помочь при составлении запроса на поиск пары):')
            print(f'Полное имя: {lovefinder_data["fullname"]}\nПол: {lovefinder_data["sex"]}'
                  f'\nДата рождения: {lovefinder_data["bdate"]} (возраст {lovefinder_data["age"]})\n'
                  f'Страна и город проживания: {lovefinder_data["country"]["title"]} ({lovefinder_data["city"]["title"]})'
                  f'\nВысшее образование: {lovefinder_data["university_name"]}\n')
            print('Давайте сформируем параметры поиска.')
            sex = set_search_gender()
            age_range = set_search_age()
            city = user.get_city() #city[0] - id города, city[1] - название города, city[3] - id страны
            print(f"Производим поиск людей по условиям:\nпол: '{sex[1]}'' \nвозраст: 'от {age_range[0]} до {age_range[1]}'' \nгород: '{city[1]}'")
            search_params = [sex[0], age_range,city]
            finded_users = user.users_search(search_params)
            print(f'\nНайдено {len(finded_users)}, удовлетворяющих поиску.')
            # Поиск пары по общим друзьям
            pair_by_friends = compare_data(lovefinder_data, finded_users, 'friends_list', 'common_friends')
            # Поиск пары по общим группам
            pair_by_groups = compare_data(lovefinder_data, finded_users, 'groups_list', 'common_groups')
            # Поиск пары по точнному возрасту
            pair_by_age = compare_data(lovefinder_data, finded_users, 'age', 'common_age')
            print(f'\nКороткая справка о пользователе:')
            print(f'Полное имя: {lovefinder_data["fullname"]}\nПол: {lovefinder_data["sex"]}\n'
                  f'Дата рождения: {lovefinder_data["bdate"]} (возраст {lovefinder_data["age"]})\n'
                  f'Страна и город проживания: {lovefinder_data["country"]["title"]} ({lovefinder_data["city"]["title"]}\n)'
                  f'Высшее образование: {lovefinder_data["university_name"]}\n'
                  f'Интересы: {lovefinder_data["interests"]}\n'
                  f'Музыка: {lovefinder_data["music"]}\n'
                  f'Фильмы: {lovefinder_data["movies"]}\n'
                  f'Книги: {lovefinder_data["books"]}\n'
                  f'О себе: {lovefinder_data["personal"]}\n'
                  f'Группы: {lovefinder_data["groups"]}\n'
                  f'Друзья: {lovefinder_data["friends_list"]}\n')
            print(f"Программа выполнена. Данные записаны в файл {os.path.join(os.path.abspath('files'))}\diplom.json")
        else:
            sys.exit(f"Что-то пошло не так :( пользователь удалил свою страницу.")
    else:
        sys.exit(f"Что-то пошло не так :( {lovefinder_data['error']}")


if __name__ == "__main__":
    start_programm()
