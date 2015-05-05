import sys
import random
import string
import logging
import importlib


def generate_name(n=4):
    return u''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(n)
    )


def get_func(name):
    module_name, attribute = name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, attribute)


def setup_loghandlers(level='DEBUG'):
    logger = logging.getLogger()
    logger.setLevel(level)
    formatter = logging.Formatter(u'%(asctime)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
