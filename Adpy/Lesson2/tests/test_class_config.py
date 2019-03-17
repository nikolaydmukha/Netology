import unittest
from Lesson2.helpers.config import Config


class TestConfig(unittest.TestCase):
    def test_output(self):
        print(Config.init_env_config_path())
        #self.assertRaises(TypeError, Config.init_env_config_path(), 2)
        self.assertTrue(Config.init_env_config_path() == "Проверка на вывод данных", "Неправильный вывод на ....!!")

    def test_out_types(self):
        self.assertRaises(TypeError, Config.init_env_config_path(), ['проверка', 'что', 'список'])

if __name__ == '__main__':
    unittest.main()
