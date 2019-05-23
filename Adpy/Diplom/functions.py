import time
import re


def set_search_gender():
    """ Установка параметров поиска: пол """
    sex = []
    while True:
        try:
            print("Укажите пол:\n    1 - женский, 2 - мужской")
            sex_input = int(input().strip())
            if (sex_input != 1) and (sex_input != 2):
                print("Вы выбрали не один из предложенных вариантов. Повторите выбор.")
                continue
        except ValueError:
            print("А-яй, вы ввели не число. Повторите ввод.")
            continue
        else:
            break
    if sex_input == 1:
        return [sex_input, 'женский']
    return [sex_input, 'мужской']


def set_search_age():
    """ Установка параметров поиска: диапазон возраста """
    age = []
    while True:
        try:
            print('Возраст от: ')
            age_from = int(input().strip())
            if age_from <= 0 or age_from >= 100:
                print("Возраст не может быть отрицательным, равным 0 и, вероятно, недвузначным.")
                continue
            break
        except ValueError:
            print("А-яй, вы ввели не число. Повторите ввод.")
            continue
    age.append(age_from)
    while True:
        try:
            print('Возраст до: ')
            age_to = int(input().strip())
            if age_to < age_from or age_to > 100:
                print("Возраст 'до' не может быть больше возраста 'от' и, вероятно, недвузначным..")
                continue
            age.append(age_to)
            break
        except ValueError:
            print("А-яй, вы ввели не число. Повторите ввод.")
            continue
    return age


def compare_users(loverfinder, finded_users, filter_by, result):
    """ Поиск пары по критериям: общие друзья, общие группы, общие интересы, общая музыка """
    for key, data in finded_users.items():
        if data[filter_by]:
            if filter_by == 'age':
                if finded_users[key][filter_by] == loverfinder[filter_by]:
                    finded_users[key][result] = loverfinder[filter_by]
                else:
                    finded_users[key][result] = ''
            elif data[filter_by] == 'photos_url':
                finded_users[key]['photos_url'] = data['photos_url']
            else:
                if set(finded_users[key][filter_by]) & set(loverfinder[filter_by]):
                    finded_users[key][result] = len(set(finded_users[key][filter_by]) & set(loverfinder[filter_by]))
                else:
                    finded_users[key][result] = ''
        else:
            finded_users[key][result] = ''
    return finded_users


def regex_compare(loverfinder, finded_users, filter_by, result):
    """ Поиск друзей по интересам: музыка, фильмы, книги """
    if filter_by in ['music', 'books', 'movies']:
        parsed_interesrts = []
        interests = loverfinder[filter_by].split(",")  # разделим полученное из запрсоа значение поля на отдельные части
        parsed_interesrts = [x.strip(' ') for x in interests]  # удалим пробельные символы слева и справа, если они есть
        regexes = list(set(filter(None, parsed_interesrts)))  # удаляем пустые и повторные элементы в списке
        regexes_modified = [val.strip('"').strip() for val in regexes]
        expression = '|'.join('\w*(?:{0})\w*'.format(x) for x in regexes_modified)
        combined_regex = re.compile(expression)
        for key, data in finded_users.items():
            if loverfinder[filter_by]:
                if filter_by in data.keys():
                    find_common = combined_regex.findall(data[filter_by])
                    if len(find_common) != 0:
                        finded_users[key][result] = find_common
                    else:
                        finded_users[key][result] = ''
                else:
                    finded_users[key][result] = ''
            else:
                finded_users[key][result] = ''
    return finded_users


def exact_result(finded_users):
    """
    Функция формирования итоговой выборки
    Требуется 10 человек, при этом:
    1. совпадение по возрасту важнее общих групп.
    2. интересы по музыке важнее книг.
    3. наличие общих друзей важнее возраста,
    Т.е.:
    1. Друзья --> 2. Возраст --> 3. Группы --> 4. Музыка --> 5. Книги --> 6. Кино
    Расположим людей в списке в очередности по логике, описанной выше.
    ВНИМАНИЕ! Если найденные пользователи не совпадают ни по каким параметрам, то выводим тех, кого нашли в первой
    выборке
    """
    users_by_id = {}
    all_another_users_from_db_by_id = {}
    for users in finded_users:
        for key, data in users.items():
            if data['common_friends']:
                users_by_id[data['id']] = [key]
            elif data['common_age']:
                users_by_id[data['id']] = [key]
            elif data['common_groups']:
                users_by_id[data['id']] = [key]
            elif data['common_music']:
                users_by_id[data['id']] = [key]
            elif data['common_books']:
                users_by_id[data['id']] = [key]
            elif data['common_movies']:
                users_by_id[data['id']] = [key]
            else:
                all_another_users_from_db_by_id[data['id']] = [key]
    users_by_id.update((all_another_users_from_db_by_id))
    return users_by_id


# Деократор для повторения выполнения запросов в случае ошибок
class RetryException(Exception):
    pass


def retry_on_error(f):
    def wrapper(*args, **argv):
        countdown = 5
        while True:
            try:
                data = f(*args, **argv)
                request_exceeded = False
                # if 'error' in data:
                #     if data['error']['error_code'] == 6:
                #         request_exceeded = True
                #     else:
                #         request_exceeded = False
                assert not request_exceeded, "Too many requests per second. We are waiting for 1 sec"
                return data
            #except AssertionError:
            except RetryException:
                if countdown <= 0:
                    raise
                countdown -= 1
                print("Слишком частые обращения к серверу. Пауза 1 сек...")
                time.sleep(1)
                continue
    return wrapper
