import os
import sys
from functions import VKUser, set_search_gender, set_search_age, compare_users, regex_compare, exact_result, write_json
from func_db import connect, create_tables, insert_users, get_users
from constants import finded_users,sasha #  УБРАТЬ В КОНЦЕ
from pprint import pprint


def start_programm():
    ##user = VKUser(sys.argv[1])
    ##print(sys.argv[1])
    #username = "155686070"
    username = "29827545"
    #username = sys.argv[1]
    user = VKUser(username)
    lovefinder_data = user.lovefinder_info()
    ###lovefinder_data = sasha
    if 'error' not in lovefinder_data.keys():
        if 'reason' not in lovefinder_data.keys():
            print(f'Привет! Сейчас мы будем искать пару пользователю с идентификатором соцсети VK "{username}".\n'
                  f'Короткая справка о пользователе (может помочь при составлении запроса на поиск пары):')
            print(f'Полное имя: {lovefinder_data["fullname"]}\nПол: {lovefinder_data["sex"]}'
                  f'\nДата рождения: {lovefinder_data["bdate"]} (возраст {lovefinder_data["age"]})\n'
                  f'Страна и город проживания: {lovefinder_data["country"]["title"]} ({lovefinder_data["city"]["title"]})'
                  f'\nВысшее образование: {lovefinder_data["university_name"]}\n')
            print('Давайте сформируем параметры поиска.')
            sex = set_search_gender()
            age_range = set_search_age()
##            city = user.get_city()  # city[0] - id города, city[1] - название города, city[2] - id страны
            city = [721, 'Власиха', 1]
##            search_params = [sex[0], age_range,city]
            # Поиск людей по городу, диапазону возраста
            ###!!!!####finded_users = user.users_search(search_params)
            print(f'\nКороткая справка о пользователе:')
            print(f'Полное имя: {lovefinder_data["fullname"]}\nПол: {lovefinder_data["sex"]}\n'
                  f'Дата рождения: {lovefinder_data["bdate"]} (возраст {lovefinder_data["age"]})\n'
                  f'Страна и город проживания: {lovefinder_data["country"]["title"]} ({lovefinder_data["city"]["title"]})\n'
                  f'Высшее образование: {lovefinder_data["university_name"]}\n'
                  f'Интересы: {lovefinder_data["interests"]}\n'
                  f'Музыка: {lovefinder_data["music"]}\n'
                  f'Фильмы: {lovefinder_data["movies"]}\n'
                  f'Книги: {lovefinder_data["books"]}\n'
                  f'Группы: {len(lovefinder_data["groups_list"])}\n'
                  f'Друзья: {len(lovefinder_data["friends_list"])}\n')
            print(f'\nНайдено {len(finded_users)}, удовлетворяющих поиску:')
            print(f"Производим поиск людей по условиям:\nпол: '{sex[1]}'' \nвозраст: 'от {age_range[0]} до "
                  f"{age_range[1]}'' \nгород: '{city[1]}'")
            if finded_users:
                # Сформируем словарь, в котором отображены найденные по критериям (возраст, город, страна)
                # люди, имеющие общих друзей, группы, музыку, книги, фильмы с тем, для кого ищем
                filter_dict = {
                    'friends_list': 'common_friends',
                    'groups_list': 'common_groups',
                    'age': 'common_age',
                    'music': 'common_music',
                    'books': 'common_books',
                    'movies': 'common_movies'
                }
                for filter_by, result in filter_dict.items():
                    if filter_by in ['friends_list', 'groups_list', 'age']:
                        pair_by = compare_users(lovefinder_data, finded_users, filter_by, result)
                    else:
                        pair_by = regex_compare(lovefinder_data, finded_users, filter_by, result)
                temp = []
                temp_dict = {}
                for name, option in pair_by.items():
                    temp_dict[name] = {}
                    temp_dict[name]['id'] = option['id']
                    temp_dict[name]['common_age'] = option['common_age']
                    temp_dict[name]['common_groups'] = option['common_groups']
                    temp_dict[name]['common_friends'] = option['common_friends']
                    temp_dict[name]['common_music'] = option['common_music']
                    temp_dict[name]['common_books'] = option['common_books']
                    temp_dict[name]['common_movies'] = option['common_movies']
                    temp_dict[name]['age_from'] = age_range[0]
                    temp_dict[name]['age_to'] = age_range[1]
                    temp_dict[name]['city_id'] = city[0]
                    temp_dict[name]['country_id'] = city[2]
                    ###print(temp_dict[name]['common_music'])
                temp.append(temp_dict)
                ###pprint(temp)
                write_json(temp)
                result_data = exact_result(temp)
                # Запись в БД
                #######connect()
                create_tables()
                insert_users(lovefinder_data, temp, result_data)
                get_users()
                print(f"Программа выполнена. Данные записаны в файл {os.path.join(os.path.abspath('files'))}\diplom.json")
            else:
                print("Не найдено ни одного человека, удовлетворяющего критериям поиска")
        else:
            sys.exit(f"Что-то пошло не так :( пользователь удалил свою страницу.")
    else:
        sys.exit(f"Что-то пошло не так :( {lovefinder_data['error']}")


if __name__ == "__main__":
    start_programm()
