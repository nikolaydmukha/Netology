import unittest
from Diplom.functions import VKUser, set_search_age
from Diplom.func_db import config_db
import os, sys, psycopg2


class TestDiplom(unittest.TestCase):
    def setUp(self):
        user_id = 'dmukha'
        self.test_class = VKUser(user_id)
        self.test_config_db = config_db
        self.test_get_city = self.test_class.get_city

    # Проверим, что результат функции lovefinder_info - нужный нам для дальнейшей работы тип dict
    def test_type_lovefinder(self):
        self.assertIsInstance(self.test_class.lovefinder_info(), dict)

    # Проверим, что результат функции get_city - тип список из 3 элементов(название города, id города, if страны)
    def test_type_get_city(self):
        self.assertEqual(len(self.test_get_city()), 3)

    # Проверка, что из конфига БД получаем нужные нам данные
    def test_config_db(self):
        os.chdir('..')
        filename = os.path.abspath('database.ini')
        section = 'postgresql'
        data = {'database': 'AdPyDiplom',
                'host': 'localhost',
                'password': 'nd$6482',
                'user': 'postgres'}
        self.assertEqual(data, self.test_config_db(filename=filename, section=section))


if __name__ == '__main__':
    unittest.main()
