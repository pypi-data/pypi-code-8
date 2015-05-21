import unittest
from open_weather_forecast.get_temperature import get_temperature


class GetTemperatureTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://api.openweathermap.org/data/2.5/forecast/city?q=London,uk'

    def tearDown(self):
        pass

    def basic_test(self):
        get_temperature(self.url, given_keys)