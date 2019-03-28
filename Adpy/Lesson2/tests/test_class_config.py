import unittest
from Lesson2.helpers.config import Config
import sys


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.test = Config.init_env_config_path()
        self.test_class = Config()

    # проверим, что установились переменные config_file и config_path
    def test_check_config_params(self):
        self.assertEqual(self.test_class.config_file, "testapp.yaml", "Не задан config_file!")
        self.assertNotEqual(self.test_class.config_paths, [], "Не задан config_paths!")

    # проверка, что вывод функции init_env_config_path() для windows состоитиз 5 значения
    @unittest.skipIf('lin' in sys.platform, 'Only for Win')
    def test_compare_list(self):
        self.assertEqual(len(self.test), 5)

    # проверка, что результаты работы функции init_env_config_path() для windows - тип list
    @unittest.skipIf('lin' in sys.platform, 'Only for Win')
    def test_output_type_true(self):
        self.assertIsInstance(self.test, list)

    # проверка результата работы функции get_verbosity_level
    def test_log_verbose(self):
        self.assertEqual(self.test_class.get_verbosity_level('critical'), 50,
                         "Некорреткно определяется уровень логирования для critical")
        self.assertEqual(self.test_class.get_verbosity_level('console'), 10,
                         "Некорреткно определяется уровень логирования для console")
        self.assertEqual(self.test_class.get_verbosity_level('warning'), 30,
                         "Некорреткно определяется уровень логирования для warning")
        self.assertEqual(self.test_class.get_verbosity_level('debug'), self.test_class.get_verbosity_level('console'),
                         "Некорреткно определяется уровень логирования для debug")
        self.assertIsInstance(self.test_class.get_verbosity_level(), str)

    # проверим, что системный диск именно C:, а не D: или другой (для windows)
    @unittest.skipIf('lin' in sys.platform, 'Only for Win')
    def test_system_disk(self):
        self.assertTrue(Config.get_windows_system_disk().rstrip(":") == "C", "Внимание! Системный диск не C:")



if __name__ == '__main__':
    unittest.main()
