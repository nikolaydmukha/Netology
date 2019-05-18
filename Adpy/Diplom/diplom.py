import sys
from functions import set_search_gender, set_search_age, compare_users, regex_compare, exact_result
from vk_user import VKUser
from func_db import create_tables, insert_users, get_users


def start_programm():
    user = VKUser(sys.argv[1])
    lovefinder_data = user.lovefinder_info(sys.argv[1])
    if 'error' not in lovefinder_data:
        if 'reason' not in lovefinder_data:
            print(f'Привет! Сейчас мы будем искать пару пользователю с идентификатором соцсети VK "{sys.argv[1]}".\n'
                  f'Короткая справка о пользователе (может помочь при составлении запроса на поиск пары):')
            print(f'Полное имя: {lovefinder_data["fullname"]}\nПол: {lovefinder_data["sex"]}'
                  f'\nДата рождения: {lovefinder_data["bdate"]} (возраст {lovefinder_data["age"]} полных лет)\n'
                  f'Страна и город проживания: {lovefinder_data["country"]["title"]} '
                  f'({lovefinder_data["city"]["title"]})\nВысшее образование: {lovefinder_data["university_name"]}\n')
            print('Давайте сформируем параметры поиска.')
            sex = set_search_gender()
            age_range = set_search_age()
            city = user.get_city()  # city[0] - id города, city[1] - название города, city[2] - id страны
            # Поиск людей по городу, диапазону возраста
            finded_users = user.users_search(sex[0], age_range, city)
            print(f'\n##СПРАВКА о соискателе##')
            # Если интересы, книги, музыка, фильмы не указаны, то выведем заглушку
            music = lovefinder_data['music'] if lovefinder_data['music'] else 'не указано'
            books = lovefinder_data['books'] if lovefinder_data['books'] else 'не указано'
            movies = lovefinder_data['movies'] if lovefinder_data['movies'] else 'не указано'
            interests = lovefinder_data['interests'] if lovefinder_data['interests'] else 'не указано'
            print(f'Полное имя: {lovefinder_data["fullname"]}\nПол: {lovefinder_data["sex"]}\n'
                  f'Дата рождения: {lovefinder_data["bdate"]} (возраст {lovefinder_data["age"]} полных лет)\n'
                  f'Страна и город проживания: {lovefinder_data["country"]["title"]} '
                  f'({lovefinder_data["city"]["title"]})\n Высшее образование: {lovefinder_data["university_name"]}\n'
                  f'Интересы: {interests}\n'
                  f'Музыка: {music}\n'
                  f'Фильмы: {movies}\n'
                  f'Книги: {books}\n'
                  f'Группы: {len(lovefinder_data["groups_list"])}\n'
                  f'Друзья: {len(lovefinder_data["friends_list"])}\n')
            print(f"##ПОИСК##\nПоиск по указанным критериям (пол: '{sex[1]}',' возраст: 'от {age_range[0]} до "
                  f"{age_range[1]}',' город: '{city[1]}')...\nВыберем из них "
                  f"подходящих людей по такой логике: друзья -> возраст -> группы -> музыка -> книги -> кино...")
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
                temp_dict = dict()
                for name, option in pair_by.items():
                    temp_dict[name] = dict()
                    for identificator in ['id', 'common_age', 'common_groups', 'common_friends', 'common_music',
                                          'common_books', 'common_movies', 'photos_url']:
                        temp_dict[name][identificator] = option[identificator]
                    temp_dict[name]['age_from'] = age_range[0]
                    temp_dict[name]['age_to'] = age_range[1]
                    temp_dict[name]['city_id'] = city[0]
                    temp_dict[name]['country_id'] = city[2]
                temp.append(temp_dict)
                result_data_find = exact_result(temp)
                create_tables()
                # Преждем, чем вставлять данные, получим тех, кто уже есть в базе по введённым критериям поиска
                result_data_in_db = get_users(lovefinder_data, age_range[0], age_range[1])
                # Исключим с помощью set() тех, кто есть в базе, из найденных людей
                # result_data_find - найденные по условиям поиска
                # result_data_in_db - найденные в базе
                set_result_data_find = set(result_data_find)
                set_result_data_in_db = set(result_data_in_db)
                set_result_data_find -= set_result_data_in_db
                if not set_result_data_find:
                    sys.exit("Ни одного нового человека, удовлетворяющего критериям поиска, не нашли. Только те, "
                             "кто уже попадался в поиск ранее!")
                # Вставим данные в БД
                insert_users(lovefinder_data, temp, list(set_result_data_find))

                print(f"Программа выполнена. Данные записаны  в базу.")
            else:
                print("Не найдено ни одного человека, удовлетворяющего критериям поиска")
        else:
            sys.exit(f"Что-то пошло не так :( Пользователь удалил свою страницу.")
    else:
        sys.exit(f"Что-то пошло не так :( {lovefinder_data['error']}")


if __name__ == "__main__":
    start_programm()
