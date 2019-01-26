"""Задача №3
Расширить домашние задание из лекции 1.4 «Функции — использование встроенных и создание собственных» новой функцией,
выводящей имена всех владельцев документов. С помощью исключения KeyError проверяйте, если поле "name" и документа.
"""
import sys

# DATA-блок
documents = [
        {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
        {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
        {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
      ]
directories = {
        '1': ['2207 876234', '11-2'],
        '2': ['10006'],
        '3': []
      }
# Блок с функциями
# Функция p
def name_by_docnumber(doc_number, return_data="\nПо указанным данным человек не найден."):
  """  search person name by document number """
  for element in documents:
    if doc_number in element.values():
      return_data = ">>> Документы с №{} соответстуют {}".format(doc_number,element["name"])
      break
  return return_data

# Функция l
def show_all_data():
  """ show all persons data from base """
  for element in documents:
    print("Тип документа: {}\nНомер документа: {}\nФИО: {}\n".format(element["type"],element["number"],element["name"]))

# Функция s
def show_shelf(doc_number, return_data="\nНет пользовательских документов."):
  """ search shelf by document number """
  for shelf_key, shelf_value in directories.items():
    if doc_number in shelf_value:
      #return_data = ">>> Документы с №{} лежат на полке №{}".format(doc_number,shelf_key)
      return_data = shelf_key
      break
  return return_data

# Функция a
def add_new(name, dt, dn, ds):
  """ add new persons data """
  new = {
    "type": dt,
    "number": dn,
    "name": name
  }
  documents.append(new)
  if ds in directories.keys():
    directories[ds].append(dn)
  else:
    directories[ds] = list()
    directories[ds].append(dn)

# Функция d
def delete_data(doc_number,return_data="\nПо указанным данным человек не найден."):
  """  delete person data by document number """
  counter = 0
  for element in documents:
    if doc_number in element.values():
      del documents[counter]
      return_data = "\n Данные пользователя удалены. Оставшихся можно посмотреть, нажав цифру 2 в меню программы!"
      break
    counter += 1
  for shelf_key, shelf_value in directories.items():
    if doc_number in shelf_value:
      directories[shelf_key].remove(doc_number)
      break
  return return_data

# Функция m
def move_data(doc_number, current, target):
  """ move data from one shelf to another"""
  print("Перемещение {} с {} на {}...".format(doc_number, current, target))
  for shelf_key, shelf_value in directories.items():
    if doc_number in shelf_value:
      directories[shelf_key].remove(doc_number)
      break
  if target in directories.keys():
    directories[target].append(doc_number)
  else:
    directories[target] = list()
    directories[target].append(doc_number)

# Функция as
def add_shelf(shelf):
  if shelf in directories.keys():
    print("Такая полка уже есть!")
  else:
    directories[shelf] = list()
    print("Полка добавлена.")

# Функция провреки ключа в словаре человека
def check_key(check):
    counter = 1
    for row in documents:
        try:
            row[check]
            print("Ключ '{}' есть в словаре {} человека!".format(check, counter))
            counter += 1
        except KeyError:
            print("Ключа '{}' в словаре {} человека нет!".format(check, counter))
            counter += 1
#    return result

# Функция управления
def action_func(action):
  if action == 1:
    doc_num = input("Введите номер искомый номер документа: ")
    p = name_by_docnumber(doc_num)
    print(p)
  elif action == 2:
    l = show_all_data()
  elif action == 3:
    doc_num = input("Введите искомый номер документа: ")
    s = show_shelf(doc_num)
    if "Нет" in s:
      print(s)
    else:
      print(">>> Документы с №{} лежат на полке №{}".format(doc_num,s))
  elif action == 4:
    name = input("Введите имя: ")
    document_type = input("Введите тип документа: ")
    document_number  = input("Введите номер документу: ")
    document_shelf = input("Введите номер полка хранения: ")
    a = add_new(name, document_type, document_number, document_shelf)
  elif action ==5:
    doc_num = input("Введите номер искомый номер документа: ")
    d = delete_data(doc_num)
  elif action == 6:
    doc_num = input("Введите искомый номер документа: ")
    target = input("Введите полку назначения: ")
    current = show_shelf(doc_num)
    if "Нет" in current:
      print(current)
    else:
      m = move_data(doc_num, current, target)
  elif action == 7:
    shelf = input("Введите номер новой полки: ")
    a_s = add_shelf(shelf)
  elif action == 8:
    check = input("Введите искомый ключ словаря: ")
    check_key(check)
  elif action == 0:
    sys.exit()

# Основная программа
stop = 1
while stop != 0:
    action = input("""\nНажмите:
    1 - для поиска человека по номеру документа;
    2 - для просмотра всех записей;
    3 - для поиска полки хранения докумнетов;
    4 - для добавления новых данных;
    5 - для удаления пользовательских данных;
    6 - для перемещения с полки на полку;
    7 - для добавления новой полки;
    8 - для проверки ключей словаря;
    0 - ВЫХОД
    """)
    action_func(int(action))