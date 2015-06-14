"""
Calculates birth information based on a specified DOB.

Displays:
    Age with 'age' function,
    Age in Days with 'age_days' function,
    Age in Hours with 'age_hours' function,
    Age in Months with 'age_months' function,
    Age in Weeks with 'age_weeks' function,
    Age in Weeks/Days with 'age_weeks_days' function,
    Age in Years/Months with 'age_years_months' function,
    Max and Min socially acceptable dating ages with 'dating_ages' function,
    Day Of Birth with 'day_of_birth' function,
    Days Since Last Birthday with 'last_birthday' function,
    Days Until Next Birthday with 'next_birthday' function.
"""

from datetime import datetime

__author__ = "Ali Raja"
__copyright__ = "Copyright 2013-2015, Ali Raja"
__credits__ = ["Ali Raja", "Ismail Ahmed", "Salim Abdala"]
__license__ = "GPL, Version 3. <http://www.gnu.org/licenses/gpl-3.0.txt>"
__version__ = "3.5.0"
__maintainer__ = "Ali Raja"
__email__ = "alir6716@gmail.com"
__status__ = "Production"

__all__ = [  # CLASSES
             "AgeCalc",
             # FUNCTIONS
             "age", "age_days", "age_hours", "age_months", "age_weeks",
             "age_weeks_days", "age_years_months", "dating_ages",
             "day_of_birth", "last_birthday", "next_birthday"
             ]

now = datetime.now()


class Current:
    def __init__(self):
        pass

    dd = now.day
    mm = now.month
    yy = now.year


class AgeCalc:
    """
    Stores DOB data into a class.

    dd: Day
    mm: Month
    yy: Year

    Note: Dates should be passed as integers.
    If the Date/Month contains a "0" before the integer, the "0" should be
        omitted.
    E.G. DOB "01/02/2000" should be passed as:
        DD: 1
        MM: 2
        YY: 2000
    """

    def __init__(self, dd, mm, yy):
        self.dd = int(dd)
        self.mm = int(mm)
        self.yy = int(yy)

    @property
    def age(self):
        ag = Current.yy - self.yy
        if self.mm > Current.mm:
            ag -= 1
        elif self.mm < Current.mm:
            pass
        else:
            if self.dd < Current.dd:
                pass
            elif self.dd > Current.dd:
                ag -= 1
            else:
                pass
        return ag

    @property
    def age_days(self):
        ad = now
        ad -= datetime(self.yy, self.mm, self.dd)
        ad = ad.days
        return ad

    # The integer returned using the property below isn't very accurate,
    #   because it simply performs the calculation age_hours*24.
    @property
    def age_hours(self):
        ah = self.age_days
        ah *= 24
        return ah

    @property
    def age_months(self):
        am = Current.yy - self.yy
        am *= 12
        am += Current.mm - self.mm
        return am

    @property
    def age_weeks(self):
        aw = self.age_days
        aw /= float(7)
        aw = int(aw)
        return aw

    # Thanks to twohot for the rounding method used below.
    # (http://stackoverflow.com/a/28081354).
    @property
    def age_weeks_days(self):
        aw = self.age_days
        aw /= float(7)
        awi = int(aw)
        aws = aw - awi
        aws *= 7
        awsr = aws // 1  # Round float up if >=0.5, down if <0.5.
        awsr += (aws % 1) / float(0.5)
        awsr = awsr // 1
        awsr = int(awsr)
        aw = int(aw)
        return dict(
            weeks=aw,
            days=awsr
        )

    @property
    def age_years_months(self):
        ag = self.age
        months = self.age_months
        months -= (ag * 12)
        return dict(
            years=ag,
            months=months
        )

    # Formulas used to determine results in the following function
    #   are available here: http://bit.ly/1cUiufu
    @property
    def dating_ages(self):
        aym = self.age_years_months
        years = aym["years"]
        months = aym["months"]
        agf = years + (months / float(12))
        mi = (agf + 14) / 2
        ma = (agf - 7) * 2
        return dict(
            max=round(ma, 1),
            min=round(mi, 1),
            original=round(agf, 1)
        )

    @property
    def day_of_birth(self):
        db = datetime(self.yy, self.mm, self.dd)
        db = db.strftime("%A")
        return db

    @property
    def last_birthday(self):
        dlb = now
        dlb -= datetime(Current.yy, self.mm, self.dd)
        dlb = dlb.days
        if str(dlb)[0] == "-":
            dlb = now
            dlb -= datetime(Current.yy - 1, self.mm, self.dd)
            dlb = dlb.days
        return dlb

    @property
    def next_birthday(self):
        dnb = datetime(Current.yy, self.mm, self.dd)
        dnb -= now
        dnb = dnb.days + 1
        if str(dnb)[0] == "-":
            dnb = datetime(Current.yy + 1, self.mm, self.dd)
            dnb -= now
            dnb = dnb.days + 1
        return dnb


def display_all(dd, mm, yy):
    """
    Returns all calculations, in a dictionary.
    See AgeCalc description for details.
    """
    ac = AgeCalc(dd, mm, yy)
    return dict(
        age=ac.age,
        age_days=ac.age_days,
        age_hours=ac.age_hours,
        age_months=ac.age_months,
        age_weeks=ac.age_weeks,
        age_weeks_days=ac.age_weeks_days,
        age_years_months=ac.age_years_months,
        dating_ages=ac.dating_ages,
        last_birthday=ac.last_birthday,
        next_birthday=ac.next_birthday
    )


def age(dd, mm, yy):
    """
    Find age in years by inputting a date of birth.
    """
    return AgeCalc(dd, mm, yy).age


def age_days(dd, mm, yy):
    """
    Find age in days by inputting a date of birth.
    """
    return AgeCalc(dd, mm, yy).age_days


def age_hours(dd, mm, yy):
    """
    Find age in hours by inputting a date of birth.
    """
    return AgeCalc(dd, mm, yy).age_hours


def age_months(dd, mm, yy):
    """
    Find age in months by inputting a date of birth.
    """
    return AgeCalc(dd, mm, yy).age_months


def age_weeks(dd, mm, yy):
    """
    Find age in weeks by inputting a date of birth.
    """
    return AgeCalc(dd, mm, yy).age_weeks


def age_weeks_days(dd, mm, yy):
    """
    Find age in weeks and days by inputting a date of birth.
    Returns a dictionary with 'weeks', 'days' keys, containing these values.
    """
    return AgeCalc(dd, mm, yy).age_weeks_days


def age_years_months(dd, mm, yy):
    """
    Find age in years and months by inputting a date of birth.
    Returns a dictionary with 'months', 'years' keys, containing these values.
    """
    return AgeCalc(dd, mm, yy).age_years_months


def dating_ages(dd, mm, yy):
    """
    Find minimum and maximum socially acceptable dating ages of a person
        by inputting a date of birth.
    Returns a dictionary with 'max', 'min' and 'original' keys,
        containing these values.

    Note: Will return strange results for a DOB under 14 years of age.
    """
    return AgeCalc(dd, mm, yy).dating_ages


def day_of_birth(dd, mm, yy):
    """
    Find day of birth by inputting a date of birth.
    """
    return AgeCalc(dd, mm, yy).day_of_birth


def last_birthday(dd, mm, yy):
    """
    Find days since last birthday by inputting a date of birth.
    """
    return AgeCalc(dd, mm, yy).last_birthday


def next_birthday(dd, mm, yy):
    """
    Find days until next birthday by inputting a date of birth.
    """
    return AgeCalc(dd, mm, yy).next_birthday
