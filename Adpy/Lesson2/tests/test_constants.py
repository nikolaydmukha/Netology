import unittest
from Lesson2.helpers.config import APP_NAME, WINDOWS


class TestConfigFails(unittest.TestCase):
    def test_is_os_windows(self):
        self.assertEqual(WINDOWS, True)

    def test_too_many_letters_name(self):
        limit = 4
        self.assertGreater(len(APP_NAME), limit)


if __name__ == '__main__':
    unittest.main()
