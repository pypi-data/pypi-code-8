__author__ = 'Eric Meisel'

import re  # regex
from dateutil import parser
import datetime


class NoDefaultDate(object):
    def replace(self, **fields):
        if any(f not in fields for f in ('year', 'month', 'day')):
            return None
        return datetime.datetime(2000, 1, 1).replace(**fields)


def cleanse_string(string_to_cleanse):
    # Replace the unicode replacement character with a space
    cleansed_string = string_to_cleanse.replace(unichr(65533), " ")

    # Trim and replace multiple whitespace characters with 1 space
    cleansed_string = re.sub(" +", " ", cleansed_string.strip())

    # Replace strings of "null" with a NULL value
    if re.match("^null$", cleansed_string, re.IGNORECASE):
        return None

    return cleansed_string


def cleanse_number(number_to_cleanse):
    cleansed_number = 0.00

    try:
        cleansed_number = float(number_to_cleanse)
    except ValueError:
        return None
    else:
        return cleansed_number


def cleanse_date(date_to_cleanse):
    cleansed_date = None
    success_date = False

    if not date_to_cleanse or date_to_cleanse == "" or date_to_cleanse == "0":
        success_date = True
        cleansed_date = None

    if not success_date:
        try:
            cleansed_date = parser.parse(date_to_cleanse, default=NoDefaultDate())
            success_date = True
        except ValueError:
            cleansed_date = None

    if success_date and cleansed_date is not None:
        cleansed_date = cleansed_date.date().strftime("%m/%d/%Y")

    return cleansed_date
