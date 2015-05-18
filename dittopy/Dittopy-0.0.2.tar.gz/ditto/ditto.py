__author__ = 'anass'


class Ditto(object):
    _instance = None
    _dir = []

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Ditto, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __getattr__(self, item):
        if item not in self.__dict__.keys():
            self.__dict__[item] = item
            return item
        return self.__dict__[item]

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __dir__(self):
        return self.__dict__.keys()

