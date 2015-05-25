from unittest import mock, TestCase
from unittest.mock import patch
import json
from os import path

import requests

from open_weather_forecast.conf.constants import FORECAST_WEATHER_INFORMATION_SCHEMA
from open_weather_forecast.info_extractor.get_info import GetInfo


class FilterInformationTest(TestCase):
    def setUp(self):
        current_directory = path.abspath(path.dirname(__file__))
        with open(path.join(current_directory, "fixtures/temperature_data.json")) as f:
            self.data = json.load(f)

    def tearDown(self):
        pass

    def complex_test(self):
        results = GetInfo().filter_information(self.data, FORECAST_WEATHER_INFORMATION_SCHEMA)
        self.assertEqual(results,  dict(
            list=[{'dt_txt': '2015-05-22 15:00:00', 'main': {'temp_max': 293.74, 'temp': 293.74, 'temp_min': 293.437}},
                  {'dt_txt': '2015-05-22 18:00:00', 'main': {'temp_max': 293.99, 'temp': 293.99, 'temp_min': 293.744}},
                  {'dt_txt': '2015-05-22 21:00:00', 'main': {'temp_max': 290.95, 'temp': 290.95, 'temp_min': 290.77}},
                  {'dt_txt': '2015-05-23 00:00:00', 'main': {'temp_max': 288.94, 'temp': 288.94, 'temp_min': 288.817}},
                  {'dt_txt': '2015-05-23 03:00:00', 'main': {'temp_max': 287.95, 'temp': 287.95, 'temp_min': 287.885}},
                  {'dt_txt': '2015-05-23 06:00:00',
                   'main': {'temp_max': 287.805, 'temp': 287.805, 'temp_min': 287.805}},
                  {'dt_txt': '2015-05-23 09:00:00',
                   'main': {'temp_max': 291.638, 'temp': 291.638, 'temp_min': 291.638}},
                  {'dt_txt': '2015-05-23 12:00:00',
                   'main': {'temp_max': 292.527, 'temp': 292.527, 'temp_min': 292.527}},
                  {'dt_txt': '2015-05-23 15:00:00', 'main': {'temp_max': 291.49, 'temp': 291.49, 'temp_min': 291.49}},
                  {'dt_txt': '2015-05-23 18:00:00',
                   'main': {'temp_max': 290.318, 'temp': 290.318, 'temp_min': 290.318}},
                  {'dt_txt': '2015-05-23 21:00:00',
                   'main': {'temp_max': 288.242, 'temp': 288.242, 'temp_min': 288.242}},
                  {'dt_txt': '2015-05-24 00:00:00',
                   'main': {'temp_max': 285.211, 'temp': 285.211, 'temp_min': 285.211}},
                  {'dt_txt': '2015-05-24 03:00:00',
                   'main': {'temp_max': 282.244, 'temp': 282.244, 'temp_min': 282.244}},
                  {'dt_txt': '2015-05-24 06:00:00',
                   'main': {'temp_max': 284.407, 'temp': 284.407, 'temp_min': 284.407}},
                  {'dt_txt': '2015-05-24 09:00:00',
                   'main': {'temp_max': 291.455, 'temp': 291.455, 'temp_min': 291.455}},
                  {'dt_txt': '2015-05-24 12:00:00',
                   'main': {'temp_max': 294.094, 'temp': 294.094, 'temp_min': 294.094}},
                  {'dt_txt': '2015-05-24 15:00:00', 'main': {'temp_max': 295.21, 'temp': 295.21, 'temp_min': 295.21}},
                  {'dt_txt': '2015-05-24 18:00:00',
                   'main': {'temp_max': 292.971, 'temp': 292.971, 'temp_min': 292.971}},
                  {'dt_txt': '2015-05-24 21:00:00',
                   'main': {'temp_max': 290.712, 'temp': 290.712, 'temp_min': 290.712}}])
                          )

    def basic_test(self):
        schema = {
            "message": float
        }

        results = GetInfo().filter_information(self.data, schema)
        self.assertEqual(results, {"message": 0.0139})

    def dict_as_arg_test(self):
        schema = {
            "message": float
        }
        results = {}
        GetInfo().filter_information(self.data, schema, results)
        self.assertEqual(results, {"message": 0.0139})


class HttpRetrieveTest(TestCase):

    def ok_test(self):
        answer = {"Blah": True}
        mocked = mock.MagicMock()
        mocked.ok = True
        mocked.json = mock.MagicMock(return_value=answer)

        with patch.object(requests, 'get', return_value=mocked) as mock_method:
            res = GetInfo().http_retrieve(url="")
            self.assertEqual(res, answer)

    def fail_test(self):
        mocked = mock.MagicMock()
        mocked.ok = False

        with patch.object(requests, 'get', return_value=mocked) as mock_method:
            res = GetInfo().http_retrieve(url="")
            self.assertEqual(res, None)
