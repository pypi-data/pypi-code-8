"""ohh - CLI tool for OHH project"""

from ohh.runner import Runner

DEFAULT_CONFIG = {
    'endpoint': 'http://localhost:3000',
    'token': None,
}


class OhhError(Exception):
    def __init__(self, message):
        self.message = message


__version__ = '0.1.0'
__author__ = 'Daniel Perez <daniel@claudetech.com>'
__all__ = []
