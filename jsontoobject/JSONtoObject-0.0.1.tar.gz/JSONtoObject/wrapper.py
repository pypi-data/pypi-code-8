__author__ = 'anass'


class Wrapper(object):
    """ py Object wrapping"""
    def __init__(self, obj):
        for key, val in obj.items():
            self.__setattr__(key, wrap(val))

    def __dir__(self):
        return self.__dict__.keys()


def wrap(obj):
    """Returns py object from json"""
    if isinstance(obj, dict):
        return Wrapper(obj)
    elif isinstance(obj, list):
        return [wrap(o) for o in obj]
    else:
        return obj
