import os
import yaml

DEFAULT_DIR = '../etc/'

class BaseConfig(object):

    __config = {}
    __default_dir = None

    @classmethod
    def load(cls, filename, default_path=DEFAULT_DIR):
        """
        Setup configuration
        """
        path = "%s/%s.yaml" % (default_path, filename)
        cls.__default_dir = default_path
        if os.path.exists(path):
            with open(path, 'rt') as filehandle:
                cls.__config = dict(yaml.load(filehandle.read()).items() + \
                    cls.__config.items())
        else:
            raise OSError("Config doesn't exists: %s" % path)

    @classmethod
    def get_default_path(cls):
        return cls.__default_dir

    @classmethod
    def get(cls, key, value=None):
        if key in cls.__config:
            return cls.__config.get(key, value)
        return cls.__config.get(key.upper(), value)

    @classmethod
    def get_url(cls, method):
        url = cls.__config.get('urls', {}).get(method)
        if not url:
            raise ValueError("Could not find url for method: %s" % method)
        return Config.get('api_host') + url

Config = BaseConfig()
