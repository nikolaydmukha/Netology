import os
import csv

from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
with open(os.path.abspath("phonebook_raw.csv"), encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    column_lastname = contacts_list[0][0]
    column_firstname = contacts_list[0][1]
    column_surname = contacts_list[0][2]
    column_organization = contacts_list[0][3]
    column_position = contacts_list[0][4]
    column_phone = contacts_list[0][5]
    column_email = contacts_list[0][6]
    contacts_list.pop(0)
    for data in contacts_list:
        lastname = data[0]
        firstname = data[1]
        surname = data[2]
        organization = data[3]
        position = data[4]
        phone = data[5]
        email = data[6]
        fio = lastname.split(' ')
        if len(fio) == 3:
            lastname = fio[0]
            firstname = fio[1]
            surname = fio[2]
        elif len(fio) == 2:
            lastname = fio[0]
            name_surname = fio[1].split(" ")
            if len(name_surname) == 2:
                firstname = name_surname[0]
                surname = name_surname[1]
            else:
                firstname = fio[1]
        print(f"{lastname} {firstname} {surname}")


#pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
# ваш код

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contacts_list)