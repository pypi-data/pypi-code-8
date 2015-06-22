from datetime import datetime


class NamedayMixin(object):
    NAMEDAYS = ()

    def get_nameday(self, month=None, day=None):
        """Return name(s) as a string based on given date and month.
        If no arguments given, use current date"""
        if month is None:
            month = datetime.now().month
        if day is None:
            day = datetime.now().day
        return self.NAMEDAYS[month-1][day-1]

    def get_month_namedays(self, month=None):
        """Return names as a tuple based on given month.
        If no month given, use current one"""
        if month is None:
            month = datetime.now().month
        return self.NAMEDAYS[month-1]
