import os
import csv
import re


# Читаем из csv данные, обрабатываем согласно заданию и приводим к единому стандарту номера телефонов
def csv_processing(file_name):
    # паттерн для парсинга всех телефонных номеров
    pattern = "(\+7\s|8\s|8|\+7)(\(|\s\(|)(\d{3})(|\)|\d{3}|\s\d{3})(\s|\-|)(\d{3}|\d{3}|\d{3})(\-|)(\d{2}|)(\-|)" \
              "(\d{2}|\d{2})(\d{2}|\s\(|\s|)((доб.\s\d{4}|))(\)|)"
    # читаем адресную книгу в формате CSV в список contacts_list
    with open(os.path.abspath(file_name), encoding="utf-8") as f:
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
        phone_dict_list = []  # общий список контактов(каждый контакт - словарь)
        phone_dict = {}  # каждый контакт - словарь, у которого клюс - имя контакта, а значение ключа - другой словарь
        # контакты
        # phone_dict_user = {} # словарь конкретного контакта
        for data in contacts_list:
            lastname = data[0]
            firstname = data[1]
            surname = data[2]
            organization = data[3]
            position = data[4]
            phone = data[5]
            email = data[6]
            fio = lastname.split(' ')
            fio_firstname = firstname.split(" ")
            if len(fio) == 3:
                lastname = fio[0]
                firstname = fio[1]
                surname = fio[2]
            elif len(fio) == 1 and len(fio_firstname) == 2:
                firstname = fio_firstname[0]
                surname = fio_firstname[1]
            elif len(fio) == 2:
                lastname = fio[0]
                name_surname = fio[1].split(" ")
                if len(name_surname) == 2:
                    firstname = name_surname[0]
                    surname = name_surname[1]
                else:
                    firstname = fio[1]
            if lastname + " " + firstname not in phone_dict.keys():
                phone_dict_user = {}  # словарь конкретного контакта
                phone_dict_user['lastname'] = lastname
                phone_dict_user['firstname'] = firstname
                phone_dict_user['surname'] = surname
                phone_dict_user['organization'] = organization
                phone_dict_user['position'] = position
                sub_for_phone = re.sub(pattern, r"+7 \3 \6 \8 \10 \13", str(phone))
                phone_dict_user['phone'] = sub_for_phone
                phone_dict_user['email'] = email
                phone_dict[lastname + " " + firstname] = phone_dict_user
            else:
                if not phone_dict[lastname + " " + firstname]['surname']:
                    phone_dict[lastname + " " + firstname]['surname'] = surname
                if not phone_dict[lastname + " " + firstname]['organization']:
                    phone_dict[lastname + " " + firstname]['organization'] == organization
                if not phone_dict[lastname + " " + firstname]['position']:
                    phone_dict[lastname + " " + firstname]['position'] = position
                if not phone_dict[lastname + " " + firstname]['phone']:
                    sub_for_phone = re.sub(pattern, r"+7 \3 \6 \8 \10 \13", str(phone))
                    phone_dict[lastname + " " + firstname]['phone'] = sub_for_phone
                if not phone_dict[lastname + " " + firstname]['email']:
                    phone_dict[lastname + " " + firstname]['email'] = email
        return phone_dict

# код для записи файла в формате CSV
def csv_writer(file_name, parsed_data):
    with open(file_name, "w", encoding="utf-8") as f:
        fieldnames = ["lastname", "firstname", "surname", "organization", "position", "phone", "email"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for val in parsed_data:
            writer.writerow(parsed_data[val])
