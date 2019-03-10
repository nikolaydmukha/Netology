import os
import sys


# Собственная реализация функции print
def adv_print(*args, **kwargs):
    """
    start - if is True than start than start the output from value of start
    max_line - limit symbols per line. If string is more than max_line
    print thr data on the next row;
    in_file - if is True than write the data to the file
    """
    for key, val in kwargs.items():
        if key == 'start':
            print(val)
        elif key == 'max_line':
            temp_name = ''
            sep = ' '
            if 'sep' in kwargs.keys():
                sep = kwargs['sep']
            for string in args:
                temp_name += str(string) + sep
            name = temp_name.rstrip(sep)
            if len(name) > val:
                temp_name = name
                while len(temp_name) > 0:
                    substring = temp_name[:val]
                    print(substring)
                    temp_name = temp_name[val:]
        elif key == 'in_file' and val == 1:
            with open(os.path.abspath('contacts_list'), 'a', encoding='utf-8') as f:
                f.write(name)


# Класс Контакт
class Contact:
    def __init__(self, first_name, last_name, phone, favorite=False, *args, **kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.favorite = favorite
        if kwargs:
            additional_info = {}
            for key, value in kwargs.items():
                additional_type = key
                additional_contact = value
                additional_info[additional_type] = additional_contact
            self.add_info = additional_info
        else:
            self.add_info = ''

    def __str__(self):
        if self.favorite is not None:
            if self.favorite == "да" or self.favorite is True:
                self.favorite = "да"
            else:
                self.favorite = "нет"
        # else:
        #     self.favorite = "нет"
        if self.add_info:
            add_info = ''
            for key, val in self.add_info.items():
                if type(val) == dict:
                    for key2, val2 in val.items():
                        add_info += key2 + ': ' + str(val2) + '\n'
                else:
                    add_info += key + ': ' + str(val) + '\n'
        else:
            add_info = ''
        return "Имя: {0}\nФамилия: {1}\nТелефон: {2}\nВ избранных: {3}\nДополнительная информация: \n{4}".\
            format(self.first_name, self.last_name, self.phone, self.favorite, add_info)


# Записная книга
class PhoneBook():
    def __init__(self, book_name):
        self.book_name = book_name
        self.contact_list = []

# Добавление контакта в книгу
    def add_contacts(self):
        first_name = input("Введите имя контакта: ")
        last_name = input("Введите фамилию контакта: ")
        phone_number = input("Введите телефон контакта: ")
        while True:
            is_favorite = input("Добавить в избранное?(да/нет): ")
            if is_favorite.lower() == "да" or is_favorite.lower() == "нет":
                if is_favorite == "да":
                    is_favorite = True
                else:
                    is_favorite = False
                break
            else:
                print("Неверные данные! Введите ' да' или 'нет'")
        flag = 0
        while True:
            add_info_input = input("ENTER для других способов связи или 0 для продолжения: ")
            if add_info_input == '':
                flag += 1
                add_info_dict = {}
                while True:
                    kind = input("Введите тип связи или нажмите ENTER для выхода: ")
                    if kind:
                        id = input("Введите идентификатор контакта: ")
                        add_info_dict[kind] = id
                    else:
                        break
            elif add_info_input == '0' and flag != 0:
                break
            elif add_info_input == '0' and flag == 0:
                add_info_dict = {}
                break
            else:
                add_info_input = input("ENTER для других способов связи или 0 для продолжения: ")
        self.contact_list.append(Contact(first_name, last_name, phone_number, is_favorite, add_info=add_info_dict))

# Вывод контактов из книги
    def show_contacts(self):
        for item in self.contact_list:
            print(item)

# Удаление данных книги
    def del_contacts(self):
        number = input("Введите номер телефона для поиска и удаления контакта: ")
        is_deleted = False
        if len(self.contact_list) != 0:
            i = 0
            while i < len(self.contact_list):
                if number == self.contact_list[i].phone:
                    del(self.contact_list[i])
                    i -= 1
                    is_deleted = True
                i += 1
            if is_deleted:
                print("Контакты удалены!")
            else:
                print("Контакты не найдены!")
        else:
            print("В записной книге нет ни одного контака!")
# Поиск избранных контактов
    def find_fav(self):
        if len(self.contact_list) != 0:
            is_favorite = False
            i = 0
            while i < len(self.contact_list):
                if self.contact_list[i].favorite == 'да':
                    print(self.contact_list[i])
                    is_favorite = True
                i += 1
            if not is_favorite:
                print("Нет избранных контактов!")
        else:
            print("В записной книге нет ни одного контака!")
# Поиск контактов по имени и фамилии
    def find_by_name(self):
        first_name = input("Введите имя: ")
        last_name = input("Введите фамилию: ")
        if len(self.contact_list) != 0:
            is_find = False
            i = 0
            while i < len(self.contact_list):
                if self.contact_list[i].first_name == first_name and self.contact_list[i].last_name == last_name:
                    print(self.contact_list[i])
                    is_find = True
                i += 1
            if not is_find:
                print("Контакты не найдены!")
        else:
            print("В записной книге нет ни одного контака!")


# Демонстрация работы adv_print
def adv_demo():
    Nicolas = Contact('Nikolay', 'Dmukha', '+7123456789', skype='@nikolaydmukha', instagram='nikolaydm',
                      email='dmukha@mail.ru')
    Julia = Contact('Julia', 'Dmukha', '+7123456789', favorite=True, skype='butova_julia', instagram='julia_rrr',
                    email='butova@mail.ru')
    print(Nicolas)
    print(Julia)
    Jhon = Contact('Jhon', 'Smith', '+71234567809')
    print(Jhon)
    adv_print("Каждый охотник желает знать, где сидит фазан!", "А если не желает?", 1, 23, 33, '(())', sep="#_#_#_#", start="*******", max_line=15, in_file=1)
