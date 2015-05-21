import json
import requests
from functools import wraps, reduce
from requests.exceptions import RequestException
import time

URL = 'http://api.openweathermap.org/data/2.5/weather?q=London,uk'
FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast/city?q=London,uk'


def get_from_dict(data_dict, list_of_keys):
    return reduce(lambda d, k: d[k], list_of_keys, data_dict)


def set_a_dict(data_dict, list_of_keys, value):
    get_from_dict(data_dict, list_of_keys[:-1])[list_of_keys[-1]] = value


def auto_tries(exception_to_catch, tries=4, delay=3):
    """
    Decorator to auto_tries the weather info

    :param tries:
    :param delay: Expressed in seconds, the waiting time between tries
    :return:
    """
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            for internal_tries in range(tries):
                try:
                    return f(*args, **kwargs)
                except exception_to_catch:
                    time.sleep(delay)
            return None

        return f_retry

    return deco_retry


@auto_tries(RequestException, tries=4, delay=1)
def http_retrieve(url):
    r = requests.get(url)
    if r.ok:
        return r.json()
    else:
        return {}


def get_temperature(url, given_keys):
    today_temperature = http_retrieve(url)
    dictionary = dict()
    if not today_temperature:
        return False, today_temperature
    else:
        for key_set in given_keys:
            value = get_from_dict(today_temperature, key_set)
            set_a_dict(dictionary, key_set, value)


def get_temperatures(url, given_keys):
    r = requests.get(url)
    dictionary = {}
    if r.ok:
        body_res = json.loads(r.text).get('list')
        for day in body_res:
            datetime = day.get('dt_txt')
            dictionary[datetime] = {}
            for key in given_keys:
                dictionary[datetime][key] = day.get(key)
        return True, dictionary
    else:
        return False, dictionary
