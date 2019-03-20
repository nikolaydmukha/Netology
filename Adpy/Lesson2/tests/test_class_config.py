import unittest
from Lesson2.helpers.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.test = Config.init_env_config_path()
        self.test_class = Config()

    # проверим, что установились переменные config_file и config_path
    def test_check_config_params(self):
        self.assertEqual(self.test_class.config_file, "testapp.yaml", "Не задан config_file!")
        self.assertNotEqual(self.test_class.config_paths, [], "Не задан config_paths!")

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

    # проверка результата работы функции get_verbosity_level
    def test_log_verbose(self):
        self.assertEqual(self.test_class.get_verbosity_level('critical'), 50,
                         "Некорреткно определяется уровень логирования для critical")
        self.assertEqual(self.test_class.get_verbosity_level('console'), 110,
                         "Некорреткно определяется уровень логирования для console")
        self.assertEqual(self.test_class.get_verbosity_level('warning'), 330,
                         "Некорреткно определяется уровень логирования для warning")
        self.assertEqual(self.test_class.get_verbosity_level('debug'), self.test_class.get_verbosity_level('console'),
                         "Некорреткно определяется уровень логирования для debug")

    # проверим, что системный диск именно C:, а не D: или другой
    def test_system_disk(self):
        self.assertTrue(Config.get_windows_system_disk().rstrip(":") == "C", "Внимание! Системный диск не C:")


if __name__ == '__main__':
    unittest.main()
