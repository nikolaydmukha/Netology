# 1. Читаем файл
# 2. Если в строке только цифры, то это строка с количеством ингредиентов
# 3. Если в строке любые символы и нет разделителя |, то это строка с названием блюда

from pprint import pprint


# Читаем данные из файла
def read_file(path_to_file):
    cook_book = {}
    list_ingredietnts = {}
    with open(path_to_file, 'r', encoding = "utf-8") as f:
        for line in f:
            if line.strip().isdigit():
                quantity = int(line)
            elif line.strip().find("|") == -1 and line.strip():
                name = line.strip().lower()
                cook_book[name] = []
            elif line.strip().find("|") != -1:
                ingredients = line.strip().split("|")
                list_ingredietnts = {"ingredient_name": ingredients[0], "quantity": int(ingredients[1]),
                                     "measure": ingredients[2]}
                cook_book[name].append(list_ingredietnts)
    return cook_book


# Формируем списко покупок
def get_shop_list_by_dishes(dishes_list, count):
    path_to_file = "D:\Python\\Netology\\Netology\\files\cook_book.txt"
    cook_book = read_file(path_to_file)
    shopping_list = {}
    for dish in dishes_list:
        if dish not in cook_book:
            pass
        else:
            for ingredient in cook_book[dish]:
                if ingredient['ingredient_name'] not in shopping_list:
                    shopping_list[ingredient['ingredient_name']] = {'measure': ingredient['measure'],
                                                                   'quantity': ingredient['quantity'] * count}
                else:
                    all_quatity = shopping_list[ingredient['ingredient_name']]['quantity'] + ingredient['quantity'] * count
                    shopping_list[ingredient['ingredient_name']]['quantity'] = all_quatity
    if shopping_list:
        pprint(shopping_list)
    else:
        print("Блюдо не найдено!")


# Код для получения данных, необходимых программе
def start_programm():
    dishes_list = []
    while True:
        dish = input("Введите название блюда или ENTER для продолжения: ")
        if not dish:
            person_count = int(input("Введите чилсо гостей: "))
            get_shop_list_by_dishes(dishes_list, person_count)
            break
        else:
            dishes_list.append(dish.lower())


start_programm()
