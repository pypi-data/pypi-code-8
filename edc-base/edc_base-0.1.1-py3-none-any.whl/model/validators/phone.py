import re

from django.conf import settings
from django.core.exceptions import ValidationError


def phone_number(value, pattern, word):
    str_value = "%s" % (value)
    p = re.compile(pattern)
    if not p.match(str_value):
        raise ValidationError(u'Invalid {} number. Got {}.'.format(word, str_value))


def CellNumber(value):
    try:
        regex = settings.CELLPHONE_REGEX
    except AttributeError:
        regex = '^[0-9+\(\)#\.\s\/ext-]+$'
    phone_number(value, regex, 'cell')


def TelephoneNumber(value):
    try:
        regex = settings.TELEPHONE_REGEX
    except AttributeError:
        regex = '^[0-9+\(\)#\.\s\/ext-]+$'
    phone_number(value, regex, 'telephone')
