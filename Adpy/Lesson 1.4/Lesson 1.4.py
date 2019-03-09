import os
import sys
from phonebook.func import adv_print, Contact, PhoneBook, adv_demo


def run_app(key):
    if key == '0':
        sys.exit("Вы нажали кнопку выхода из программы")
    elif key == '1':
        phonebook.show_contacts()
    elif key == '2':
        phonebook.add_contacts()
    elif key == '3':
        phonebook.del_contacts()
    elif key == '4':
        phonebook.find_fav()
    elif key == '5':
        phonebook.find_by_name()
    elif key == '6':
        adv_demo()


if __name__ == '__main__':
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
            phonebook.add_contacts()
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
        6 - для демонстрации функции adv_print;
        0 - ВЫХОД
        """)
        run_app(action)




