import unittest
from open_weather_forecast.get_temperature import GetTemperature
from open_weather_forecast.constants import WEATHER_INFORMATION_SCHEMA


class GetTemperatureTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://api.openweathermap.org/data/2.5/forecast/city?q={}'.format("London,uk")

    def tearDown(self):
        pass

    def basic_test(self):
        pass