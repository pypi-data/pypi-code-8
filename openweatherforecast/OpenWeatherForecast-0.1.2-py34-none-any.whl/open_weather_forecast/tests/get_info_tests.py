import unittest
import json
from os import path
from open_weather_forecast.constants import WEATHER_INFORMATION_SCHEMA
from open_weather_forecast.get_info import GetInfo


class FilterInformationTest(unittest.TestCase):
    def setUp(self):
        current_directory = path.abspath(path.dirname(__file__))
        with open(path.join(current_directory, "fixtures/temperature_data.json")) as f:
            self.data = json.load(f)

    def tearDown(self):
        pass

    def basic_test(self):
        # pass
        results = GetInfo().filter_information(self.data, WEATHER_INFORMATION_SCHEMA)
        assert results == {'list': [{'dt_txt': '2015-05-22 15:00:00', 'main': {'temp_max': 293.74, 'temp': 293.74, 'temp_min': 293.437}}, {'dt_txt': '2015-05-22 18:00:00', 'main': {'temp_max': 293.99, 'temp': 293.99, 'temp_min': 293.744}}, {'dt_txt': '2015-05-22 21:00:00', 'main': {'temp_max': 290.95, 'temp': 290.95, 'temp_min': 290.77}}, {'dt_txt': '2015-05-23 00:00:00', 'main': {'temp_max': 288.94, 'temp': 288.94, 'temp_min': 288.817}}, {'dt_txt': '2015-05-23 03:00:00', 'main': {'temp_max': 287.95, 'temp': 287.95, 'temp_min': 287.885}}, {'dt_txt': '2015-05-23 06:00:00', 'main': {'temp_max': 287.805, 'temp': 287.805, 'temp_min': 287.805}}, {'dt_txt': '2015-05-23 09:00:00', 'main': {'temp_max': 291.638, 'temp': 291.638, 'temp_min': 291.638}}, {'dt_txt': '2015-05-23 12:00:00', 'main': {'temp_max': 292.527, 'temp': 292.527, 'temp_min': 292.527}}, {'dt_txt': '2015-05-23 15:00:00', 'main': {'temp_max': 291.49, 'temp': 291.49, 'temp_min': 291.49}}, {'dt_txt': '2015-05-23 18:00:00', 'main': {'temp_max': 290.318, 'temp': 290.318, 'temp_min': 290.318}}, {'dt_txt': '2015-05-23 21:00:00', 'main': {'temp_max': 288.242, 'temp': 288.242, 'temp_min': 288.242}}, {'dt_txt': '2015-05-24 00:00:00', 'main': {'temp_max': 285.211, 'temp': 285.211, 'temp_min': 285.211}}, {'dt_txt': '2015-05-24 03:00:00', 'main': {'temp_max': 282.244, 'temp': 282.244, 'temp_min': 282.244}}, {'dt_txt': '2015-05-24 06:00:00', 'main': {'temp_max': 284.407, 'temp': 284.407, 'temp_min': 284.407}}, {'dt_txt': '2015-05-24 09:00:00', 'main': {'temp_max': 291.455, 'temp': 291.455, 'temp_min': 291.455}}, {'dt_txt': '2015-05-24 12:00:00', 'main': {'temp_max': 294.094, 'temp': 294.094, 'temp_min': 294.094}}, {'dt_txt': '2015-05-24 15:00:00', 'main': {'temp_max': 295.21, 'temp': 295.21, 'temp_min': 295.21}}, {'dt_txt': '2015-05-24 18:00:00', 'main': {'temp_max': 292.971, 'temp': 292.971, 'temp_min': 292.971}}, {'dt_txt': '2015-05-24 21:00:00', 'main': {'temp_max': 290.712, 'temp': 290.712, 'temp_min': 290.712}}]}


class AutoTriesDecoratorTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://api.openweathermap.org/data/2.5/forecast/city?q={}'.format("London,uk")

    def tearDown(self):
        pass

    def zero_retries_test(self):
        @GetInfo.auto_tries(ValueError, tries=0, delay=0)
        def test_func():
            raise ValueError()

        self.assertEqual(test_func(), None)

    def zero_retries_no_exception_test(self):
        @GetInfo.auto_tries(ValueError, tries=0, delay=0)
        def test_func():
            return 1

        self.assertEqual(test_func(), None)

    def retries_no_exception_test(self):
        @GetInfo.auto_tries(ValueError, tries=1, delay=0)
        def test_func():
            return 1

        self.assertEqual(test_func(), 1)

    def retries_exception_test(self):
        @GetInfo.auto_tries(BaseException, tries=2, delay=0)
        def test_func():
            raise BaseException

        self.assertEqual(test_func(), None)

    def retries_wrong_exception_test(self):
        @GetInfo.auto_tries(ValueError, tries=2, delay=0)
        def test_func():
            raise KeyError

        self.assertRaises(KeyError, test_func)

