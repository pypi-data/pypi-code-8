__author__ = 'anass'


class Wrapper(object):
    """ py Object wrapping"""
    def __init__(self, obj):
        for key, val in obj.items():
            self.__setattr__(key, wrap(val))

    def __dir__(self):
        return self.__dict__.keys()

    def to_json(self):
        return {key: serialize(value) for key, value in self.__dict__.items()}


def wrap(obj):
    """Returns py object from json"""
    if isinstance(obj, dict):
        return Wrapper(obj)
    elif isinstance(obj, list):
        return [wrap(o) for o in obj]
    else:
        return obj


def serialize(value):
    if isinstance(value, Wrapper):
        return value.to_json()
    elif isinstance(value, list):
        return [o.to_json() for o in value]
    return value
