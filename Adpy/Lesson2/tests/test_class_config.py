import unittest
from Lesson2.helpers.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.test = Config.init_env_config_path()

    # проверка, что вывод функции init_env_config_path() - конкретный список значений
    def test_compare_list(self):
        #test = ['проверка', 'что', 'это', 'список']
        test = ['.\\', 'C:\\Users\\Владимир\\.testapp', 'C:\\Users\\Владимир\\AppData\\Roaming\\testapp',
                'D:\\Python\\Netology\\Netology\\Adpy\\Lesson2', 'C:\\']
        self.assertListEqual(self.test, test)

    # проверка, что результаты работы функции init_env_config_path() - тип list
    def test_output_type_true(self):
        self.assertIsInstance(self.test, list)

    # проверка, что результаты работы функции init_env_config_path() - тип dict
    def test_output_type_false(self):
        self.assertIsInstance(self.test, dict)

    # проверим, что системный диск именно C:
    def test_system_disk(self):
        self.assertTrue(Config.get_windows_system_disk().rstrip(":") == "C", "Внимание! Системный диск не C:")


if __name__ == '__main__':
    unittest.main()
