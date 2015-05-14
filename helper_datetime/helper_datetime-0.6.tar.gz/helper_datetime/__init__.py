#!/usr/bin/env python
#-*- coding:utf -*-
import re
import datetime
import time
import iso8601


class HelperDateTime(object):
    """
    rfc5322 Internet Message Format
    RFC 822, 1036, 1123, 2822
    3.3.  Date and Time Specification
    http://tools.ietf.org/html/rfc5322#section-3.3

    Examples:

        Wed, 25 Mar 2015 02:23:56 +0000
        Wednesday, 25-Mar-15 02:23:56 UTC


    rfc3339 Date and Time on the Internet: Timestamps
    http://tools.ietf.org/html/rfc3339

    Examples:

        1990-12-31T23:59:60Z
        1937-01-01T12:00:27.87+00:20


    http://en.wikipedia.org/wiki/ISO_8601
    http://www.iso.org/iso/home/standards/iso8601.htm

    Examples:

        2015-03-24T06:57:23+00:00
        2015-03-24T06:57:23Z
    """

    PATTERNS = [
        ur'(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})',
        ur'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})',
        ur'(?P<month>\d{2})/(?P<day>\d{2})/(?P<year>\d{2})',        
        ur'^(?P<year>\d{4})',
    ]

    def __init__(self, s, pattern=None):
        """
        >>> HelperDateTime(u'光明頂- 20150324 - 新加坡模式').date
        datetime.date(2015, 3, 24)
        """
        self._datetime = None
        self._parse_datetime(s=s, pattern=pattern)

    def _parse_datetime(self, s, pattern=None):
        if pattern:
            patterns = [pattern]
        else:
            try:
                self._datetime = iso8601.parse_date(s)
                return
            except iso8601.iso8601.ParseError:
                pass

            patterns = HelperDateTime.PATTERNS

        for pattern in patterns:
            m = re.search(pattern=pattern, string=s)
            if not m:
                continue

            group_dict = m.groupdict()

            year, month, day = 1, 1, 1
            hour, minute, second = 0, 0, 0

            if 'year' in group_dict:
                year = int(group_dict['year'])

                if (year <= 99): 
                    this_year = datetime.date.today().year % 100 
                    if this_year >= year:
                        year = 2000 + year
                    else:
                        year = 1900 + year

            if 'month' in group_dict:
                month = int(group_dict['month'])

            if 'day' in group_dict:
                day = int(group_dict['day'])

            if 'hour' in group_dict:
                hour = int(group_dict['hour'])

            if 'minute' in group_dict:
                minute = int(group_dict['minute'])

            if 'second' in group_dict:
                second = int(group_dict['second'])

            self._datetime = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
            return



    @property
    def total_seconds(self):
        return (self._datetime - datetime.datetime(1970, 1, 1)).total_seconds()

    @property
    def format_in_iso8601(self):
        """
        >>> HelperDateTime('2015-05-13T16:21:22.715Z').format_in_iso8601
        '2015-05-13T16:21:22.715000+00:00'
        """
        return self._datetime.isoformat()

    @property
    def format_in_internet_message_format_timestamp(self):
        """
        >>> HelperDateTime('2015-05-14').format_in_internet_message_format_timestamp
        'Thu, 14 May 2015 00:00:00 GMT'

        >>> HelperDateTime('2015-05-13T16:21:22.715Z').format_in_internet_message_format_timestamp
        'Wed, 13 May 2015 16:21:22 GMT'
        """
        return time.strftime("%a, %d %b %Y %H:%M:%S GMT", self._datetime.timetuple())

    @property
    def date(self):
        """
        >>> HelperDateTime('2015-05-13T16:21:22.715Z').date
        datetime.date(2015, 5, 13)

        >>> HelperDateTime('2015-05-14').date
        datetime.date(2015, 5, 14)

        >>> HelperDateTime(u'光明頂- 20150324 - 新加坡模式').date
        datetime.date(2015, 3, 24)
        """
        return datetime.date(year=self._datetime.year, month=self._datetime.month, day=self._datetime.day)

    @property
    def alias(self):
        alias_list = []

        # use 2015-04-01 as example
        alias_list.append(self.format_in_iso8601) # '2015-04-01T10:08:42.120735'

        alias_list.append(self.date.isoformat()) # 2015-04-01

        alias_list.append(self.date.isoformat().replace('-', '')) # 20150401

        f = "%s-%s-%s" % (str(self._datetime.month).zfill(2), str(self._datetime.day).zfill(2), str(self._datetime.year)[2:4])
        alias_list.append(f) # 04-01-15

        alias_list.append(f.replace('-', '/')) # 04/01/15

        return alias_list
        
    @staticmethod
    def date_range(start, end):
        """
        >>> list(HelperDateTime.date_range('20150401', '20150405'))
        [datetime.date(2015, 4, 1), datetime.date(2015, 4, 2), datetime.date(2015, 4, 3), datetime.date(2015, 4, 4), datetime.date(2015, 4, 5)]
        """
        assert len(start) == 8
        assert len(end) == 8

        yyyy = int(start[:4])
        mm = int(start[4:6])
        dd = int(start[6:])
        start_d  = datetime.date(year=yyyy, month=mm, day=dd)

        yyyy = int(end[:4])
        mm = int(end[4:6])
        dd = int(end[6:])
        end_d  = datetime.date(year=yyyy, month=mm, day=dd)

        days_offset = (end_d - start_d).days
        if days_offset < 0:
            raise Exception('start date must be older than end date')

        for day_offset in xrange(0, days_offset + 1):
            yield start_d + datetime.timedelta(days=day_offset)
            
            
if __name__ == '__main__':
    import doctest
    doctest.testmod()


