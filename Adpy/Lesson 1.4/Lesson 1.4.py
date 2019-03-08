import os
import sys


# Собственная реализация функции print
def adv_print(name, **kwargs):
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
            if len(name) > val:
                temp_name = name
                while len(temp_name) > 0:
                    substring = temp_name[:val]
                    print(substring)
                    temp_name = temp_name[val:]
        elif key == 'in_file':
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
class PhoneBook(Contact):
    def __init__(self, book_name):
        self.book_name = book_name
        self.contact_list = []

# Добавление контакта в книгу
    def add_contact(self):
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


def run_app(key):
    if key == '0':
        sys.exit("Вы нажали кнопку выхода из программы")
    elif key == '1':
        phonebook.show_contacts()


if __name__ == '__main__':
    Nicolas = Contact('Nikolay', 'Dmukha', '+7123456789', skype='@nikolaydmukha', instagram='nikolaydm', email='dmukha@mail.ru')
    Julia = Contact('Julia', 'Dmukha', '+7123456789', favorite=True, skype='butova_julia', instagram='julia_rrr', email='butova@mail.ru')
    print(Nicolas)
    print(Julia)
    jhon = Contact('Jhon', 'Smith', '+71234567809')
    print(jhon)

    adv_print("Каждый охотник желает знать, где сидит фазан!", max_line=39, in_file=1)
    name = input("Введите имя записаной книги:")
    while not name:
        name = input("Введите имя записаной книги:")
    phonebook = PhoneBook(name)
    stop = '1'
    while True:
        stop = input("ENTER для добавления контакта или 0 для выхода: ")
        if stop == '0':
            break
        elif stop == '':
            phonebook.add_contact()
        else:
            stop = input("ENTER или 0! ")
    phonebook.show_contacts()

    stop = 1
    while stop != 0:
        action = input("""\nНажмите:
        1 - для просмотра всех записей;
        2 - для добавления новых данных;
        3 - для удаления контакта по номеру телефона;
        4 - для поиска избранных контактов;
        5 - для поиска по имени и фамилии;
        0 - ВЫХОД
        """)
        run_app(action)




