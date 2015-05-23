import unittest

from open_weather_forecast.conf.constants import WEATHER_INFORMATION_SCHEMA
from open_weather_forecast.info_extractor.get_temperature import GetTemperature


class GetTemperatureTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://api.openweathermap.org/data/2.5/forecast/city?q={}'.format("London,uk")

    def tearDown(self):
        pass

    def basic_test(self):
        pass
        # get_temp_manager = GetTemperature()
        # info = get_temp_manager.http_retrieve(url=self.url)
        # get_temp_manager.filter_information(info, WEATHER_INFORMATION_SCHEMA)