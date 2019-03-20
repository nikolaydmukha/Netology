import unittest
from Lesson2.helpers.config import APP_NAME, WINDOWS, Config
from Lesson2.app import App
#from Lesson2.app import App


class TestConfigFails(unittest.TestCase):
    # проверка что ОС windows
    def test_is_os_windows(self):
        self.assertEqual(WINDOWS, True)

    # проверка, что имя приложения > 4 символов
    def test_too_many_letters_name(self):
        limit = 4
        self.assertGreater(len(APP_NAME), limit)

    # проверка, что тестовый класс - инстанс класса Config
    def test_app_isinstance_config(self):
        test_app = App()
        self.assertIsInstance(test_app.config, Config)


if __name__ == '__main__':
    unittest.main()
