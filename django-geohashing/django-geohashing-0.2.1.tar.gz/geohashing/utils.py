"""
Utility functions available to the geohashing app
"""

import csv
import datetime
import logging
import StringIO
from collections import OrderedDict

import requests

logger = logging.getLogger(__name__)

YAHOO_FINANCE_URL = "http://ichart.finance.yahoo.com/table.csv?s=DJIA&a={start_month:0>2}&b={start_day:0>2}&c={start_year}&d={end_month:0>2}&e={end_day:0>2}&f={end_year}&g=d&ignore=.csv"
MINIMUM_DJIA_DATE = datetime.date(1928, 1, 1)


class YahooFinanceDataNotFoundException(BaseException):
    """
    BaseException subclass that is raised when Yahoo Finance data is unavailable
    """
    pass


def _retrieve_csv(from_date, to_date):
    """
    Retrieve the DJIA historical data CSV from Yahoo finance.

    Note that the Yahoo API uses 0-indexed month values (Jan = 0,...)
    """

    fmt = {
        'start_year': from_date.year,
        'start_month': from_date.month - 1,
        'start_day': from_date.day,
        'end_year': to_date.year,
        'end_month': to_date.month - 1,
        'end_day': to_date.day,
    }
    url = YAHOO_FINANCE_URL.format(**fmt)
    response = requests.get(url)
    if response.status_code != 200:
        raise YahooFinanceDataNotFoundException(
            "Non 200 status returned from {}".format(url)
        )
    return StringIO.StringIO(response.content)

def _extract_data_from_csv(csvfile):
    """
    Read the DJIA opening values from a CSV file into a dictionary

    Note: The historical DJIA values provided have more precision
    than we need or want (currently 5 digits). Other geohashing
    implementations round this value to the nearest hundredth of
    a point and we will follow suit.
    """
    openings = OrderedDict()
    reader = csv.DictReader(csvfile)
    for row in reader:
        year, month, day = tuple(int(s) for s in row['Date'].split('-'))
        djia = float(row['Open'])
        openings[datetime.date(year, month, day)] = "{:.2f}".format(round(djia, 2))
    return openings

def _interpolate_djia_values(openings_dict):
    """
    Fills in holes in the opening data left by weekends and holidays

    Whenever a gap in the data is encountered, it will be filled with
    a new datetime.date key that has the value of the previous opening
    (sorted in chronological order).
    """
    min_date = min(openings_dict.keys())
    max_date = max(openings_dict.keys())
    curr_date = min_date
    one_delta = datetime.timedelta(1)
    while curr_date <= max_date:
        if curr_date not in openings_dict:
            openings_dict[curr_date] = openings_dict[curr_date - one_delta]
        curr_date += one_delta
    # And put everything into chronological order
    return OrderedDict(sorted(openings_dict.items(), key=lambda date_djia_pair: date_djia_pair[0]))

def get_historical_djia_openings(from_date=None, to_date=None):
    """
    Returns a dictionary mapping dates to DJIA opening prices

    Dates within the date range for which no opening price is
    recorded (i.e. weekends and holidays) will be interpolated
    according to the standard geohashing rules.
    """
    yesterday = datetime.date.today() - datetime.timedelta(1)
    if from_date is None:
        from_date = MINIMUM_DJIA_DATE
    if to_date is None:
        to_date = yesterday

    if from_date < MINIMUM_DJIA_DATE:
        logger.warn(
            "Records from %s requested. Only retrieving data from %s onwards",
            from_date,
            MINIMUM_DJIA_DATE
        )
        from_date = MINIMUM_DJIA_DATE

    if to_date > yesterday:
        logger.warn(
            "Records up to %s requested. Historical data through %s retrieved",
            to_date,
            yesterday
        )
        to_date = yesterday

    csvfile = _retrieve_csv(from_date, to_date)
    openings = _extract_data_from_csv(csvfile)
    min_returned_date = min(openings.keys())
    max_returned_date = max(openings.keys())
    if from_date < min_returned_date:
        logger.warn(
            "Historical prices before %s omitted.",
            str(min_returned_date)
        )
    if to_date > max_returned_date:
        logger.warn(
            "Historical prices after %s omitted.",
            str(max_returned_date)
        )
    openings = _interpolate_djia_values(openings)
    return openings
