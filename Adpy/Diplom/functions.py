import time
import re


# Установка параметров поиска: пол
def set_search_gender():
    sex = []
    while True:
        try:
            print("Укажите пол:\n    1 - женский, 2 - мужской")
            sex_input = int(input().strip())
            if (sex_input != 1) & (sex_input != 2):
                print("Вы выбрали не один из предложенных вариантов. Повторите выбор.")
                continue
        except ValueError:
            print("А-яй, вы ввели не число. Повторите ввод.")
            continue
        else:
            break
    if sex_input == 1:
        sex = [sex_input, 'женский']
    else:
        sex = [sex_input, 'мужской']
    return sex


# Установка параметров поиска: диапазон возраста
def set_search_age():
    age = []
    while True:
        try:
            print('Возраст от: ')
            age_from = int(input().strip())
            if age_from < 0 or age_from == 0 or len(str(age_from)) > 2:
                print("Возраст не может быть отрицательным, равным 0 и, вероятно, недвузначным.")
                continue
        except ValueError:
            print("А-яй, вы ввели не число. Повторите ввод.")
            continue
        else:
            age.append(age_from)
            while True:
                try:
                    print('Возраст до: ')
                    age_to = int(input().strip())
                    if age_to < age_from or len(str(age_to)) > 2:
                        print("Возраст 'до' не может быть больше возраста 'от' и, вероятно, недвузначным..")
                        continue
                except ValueError:
                    print("А-яй, вы ввели не число. Повторите ввод.")
                    continue
                else:
                    age.append(age_to)
                    break
            break
    return age


# Поиск пары по критериям: общие друзья, общие группы, общие интересы, общая музыка
def compare_users(loverfinder, finded_users, filter_by, result):
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


# Поиск друзей по интересам: музыка, фильмы, книги
def regex_compare(loverfinder, finded_users, filter_by, result):
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


# Функция формирования итоговой выборки
def exact_result(finded_users):
    """
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
    ordered_users = []
    friends, age, groups, music, movies, books, all_another = [], [], [], [], [], [], []
    for users in finded_users:
        for key, data in users.items():
            if data['common_friends']:
                friends.append(key)
            elif data['common_age']:
                age.append(key)
            elif data['common_groups']:
                groups.append(key)
            elif data['common_music']:
                music.append(key)
            elif data['common_books']:
                books.append(key)
            elif data['common_movies']:
                movies.append(key)
            else:
                all_another.append(key)
    for i in [friends, age, groups, music, books, movies, all_another]:
        ordered_users.extend(i)
    return ordered_users


# Деократор для повторения выполнения запросов в случае ошибок
def retry_on_error(f):
    def wrapper(*args, **argv):
        countdown = 5
        while True:
            try:
                print("deco")
                data = f(*args, **argv)
                request_exceeded = False
                if 'error' in data:
                    if data['error']['error_code'] == 6:
                        request_exceeded = True
                    else:
                        request_exceeded = False
                assert not request_exceeded, "Too many requests per second. We are waiting for 1 sec"
                return data
            except AssertionError:
                if countdown <= 0:
                    raise
                countdown -= 1
                print("Слишком частые обращения к серверу. Пауза 1 сек...")
                time.sleep(1)
                continue
    return wrapper
