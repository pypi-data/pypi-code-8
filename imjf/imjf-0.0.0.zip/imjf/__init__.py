""" The official Python client for www.isMyJsFucked.com """

from .client import is_my_js_fucked, report
from .exceptions import IMJFException

__all__ = ['is_my_js_fucked',
           'report',
           'IMJFException']

