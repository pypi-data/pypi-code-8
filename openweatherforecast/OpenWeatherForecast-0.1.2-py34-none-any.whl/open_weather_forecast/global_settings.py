import os
import yaml
from datetime import datetime, timedelta

from open_weather_forecast.constants import CFG_CACHE_TTL, CFG_FILE_PATH, CFG_FILE_PATH_ENV


class SettingCache():
    """ The settings cache! Borg pattern in here
    """
    __shared_state = {}

    def __init__(self, update_callback=None):
        self.__dict__ = self.__shared_state
        if update_callback is not None:
            self.update_callback = update_callback
        if not hasattr(self, 'last_update') or ((datetime.utcnow() + timedelta(seconds=self.refresh)) > self.last_update):
            self.update()

    def update(self):
        """Use as well for manual updates
        """
        self.refresh = CFG_CACHE_TTL
        self.last_update = datetime.now()
        self.cache = self.update_callback()


def get_global_settings(refresh=False):
    """Store Global config into cache to avoid to high disk access
        Cache updates every 5 secs by default
        refresh = True => Force a cache's update
    """
    sc = SettingCache()
    if refresh:
        sc.update()
    return sc.cache


def read_settings():
    """ Read global configuration yaml file
    """
    try:
        f_path = os.environ.get(CFG_FILE_PATH_ENV).strip()
        with open(f_path, 'r') as f:
            return yaml.load(f)
    except AttributeError:
        try:
            with open(CFG_FILE_PATH, 'r') as f:
                return yaml.load(f)
        except:
            msg = "Can't find settings in %s neither %s" % (CFG_FILE_PATH_ENV, CFG_FILE_PATH)
            raise Exception(msg)

SettingCache(read_settings)

