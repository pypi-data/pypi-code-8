import unittest
from open_weather_forecast.get_temperature import auto_tries


class AutoTriesDecoratorTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://api.openweathermap.org/data/2.5/forecast/city?q={}'.format("London,uk")

    def tearDown(self):
        pass

    def zero_retries_test(self):
        @auto_tries(ValueError, tries=0, delay=0)
        def test_func():
            raise ValueError()

        self.assertEqual(test_func(), None)

    def zero_retries_no_exception_test(self):
        @auto_tries(ValueError, tries=0, delay=0)
        def test_func():
            return 1

        self.assertEqual(test_func(), None)

    def retries_no_exception_test(self):
        @auto_tries(ValueError, tries=1, delay=0)
        def test_func():
            return 1

        self.assertEqual(test_func(), 1)

    def retries_exception_test(self):
        @auto_tries(BaseException, tries=2, delay=0)
        def test_func():
            raise BaseException

        self.assertEqual(test_func(), None)

    def retries_wrong_exception_test(self):
        @auto_tries(ValueError, tries=2, delay=0)
        def test_func():
            raise KeyError

        self.assertRaises(KeyError, test_func)
