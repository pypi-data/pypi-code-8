__author__ = 'Sinisa'


import os
import glob
from sbg_cli.config import Config
from sbg_cli.command import Command, Utility


__version__ = '0.1.1'


pth = os.path.dirname(__file__)
utilities = filter(lambda x: os.path.isdir(x), glob.glob(os.path.dirname(__file__) + '/*'))
__all__ = ['.'.join(f.split('/')[-2:]) for f in utilities]


def disable_warnings():
    import requests
    requests.packages.urllib3.disable_warnings()
