import json
import requests
from functools import wraps
import time

URL = 'http://api.openweathermap.org/data/2.5/weather?q=London,uk'
FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast/city?q=London,uk'


def retry(tries=4, delay=3, logger=None):
    """
    Decorator to retry the weather info

    :param tries:
    :param delay: Expressed in seconds, the waiting time between tries
    :param logger:
    :return:
    """
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            internal_tries = tries
            while internal_tries > 1:
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    msg = "{}, Retrying in {} seconds...".format(str(e), delay)
                    if logger:
                        logger.warning(msg)
                    time.sleep(delay)
                    internal_tries -= 1
            return f(*args, **kwargs)

        return f_retry

    return deco_retry


@retry(tries=4, delay=1)
def get_temperature(url=URL):
    r = requests.get(url)
    if r.ok:
        body_res = json.loads(r.text).get('main')
        return True, {'temp': body_res.get('temp'),
                      'temp_max': body_res.get('temp_max'),
                      'temp_min': body_res.get('temp_min')}
    else:
        return False, {}


def get_temperatures(given_keys):
    url = 'http://api.openweathermap.org/data/2.5/forecast/city?q=London,uk'
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


if __name__ == "__main__":
    import ipdb
    ipdb.set_trace()
    get_temperature()