__author__ = 'Alex Gomes'

import datetime, time

format_desc_human='%Y-%m-%d %H:%M:%S'

def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

def format_from_timestamp(utc_datetime):
    return str(datetime_from_utc_to_local(utc_datetime).strftime(format_desc_human))