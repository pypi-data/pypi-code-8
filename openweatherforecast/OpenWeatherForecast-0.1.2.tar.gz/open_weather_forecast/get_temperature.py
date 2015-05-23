import requests
from functools import reduce
from requests.exceptions import RequestException

from open_weather_forecast.get_info import GetInfo


class GetTemperature(GetInfo):

    @GetInfo.auto_tries(RequestException, tries=4, delay=1)
    def http_retrieve(self, url):
        r = requests.get(url)
        if r.ok:
            return r.json()
        else:
            return {}

    def get_temperature(self, url, information_schema):
        temperatures_history = self.http_retrieve(url)

        if not temperatures_history:
            return False, {}
        else:
            try:
                return True, self.filter_information(temperatures_history, information_schema)
            except (ValueError, KeyError):
                return False, {}


def get_from_dict(data_dict, list_of_keys):
    list_of_keys = [list_of_keys] if not isinstance(list_of_keys, list) else list_of_keys
    return reduce(lambda d, k: d.get(k, {}), list_of_keys, data_dict)


def set_a_dict(data_dict, list_of_keys, value):
    get_from_dict(data_dict, list_of_keys[:-1])[list_of_keys[-1]] = value