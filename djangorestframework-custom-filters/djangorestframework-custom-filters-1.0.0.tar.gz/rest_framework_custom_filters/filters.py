# -*- coding: utf-8 -*-

import django_filters
from rest_framework.exceptions import APIException
from django import forms
from django.utils.encoding import force_str
from django.utils.dateparse import parse_datetime
from rest_framework import ISO_8601
from django.conf import settings
import pytz

class IsoDateTimeField(forms.DateTimeField):
    """
    Field for date iso 8601
    """
    def __init__(self, *args, **kwargs):
        kwargs['input_formats'] = (ISO_8601, )
        super(IsoDateTimeField, self).__init__(*args, **kwargs)

    def strptime(self, value, format):
        """
        By default, parse datetime with TZ.
        If TZ is False, convert datetime to local time and disable TZ
        """

        value = force_str(value)
        if format == ISO_8601:
            try:
                parsed = parse_datetime(value)
                if not settings.USE_TZ:
                        fr_tz = pytz.timezone(settings.TIME_ZONE)
                        parsed = parsed.astimezone(fr_tz).replace(tzinfo=None)
            except:
                raise APIException(
                    "date parsing error: since parameter use the date format ISO 8601 (ex: 2014-11-18T15:56:58Z)")

            if parsed is None:
                raise APIException(
                    "since parameter use the date format ISO 8601 (ex: 2014-11-18T15:56:58Z)")
            return parsed
        return super(IsoDateTimeField, self).strptime(value, format)


class IsoDateTimeFilter(django_filters.DateTimeFilter):
    """ Extend ``DateTimeFilter`` to filter by ISO 8601 formated dates too"""
    field_class = IsoDateTimeField



