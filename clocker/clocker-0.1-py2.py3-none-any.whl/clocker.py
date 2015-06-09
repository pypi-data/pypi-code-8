"""A small Python 3 module that keeps track of elapsed time
and its current state"""

import time
import math

__version__ = '0.1'


class Clocker(object):
    """The time watcher class that keeps track of elapsed time and state"""
    def __init__(self):
        self.mode = 'init'
        self.startTime = 0
        # self.elapsed will always be in floating point seconds
        self.elapsed = 0

    def start(self):
        """Set the initial starting point and return the start Time`"""
        if self.mode == 'init':
            self.startTime = time.time()
            self.mode = "running"

        elif self.mode == 'stopped':
            self.startTime = time.time()
            self.mode = 'running'

        # if clocker is in any other modes, return None as no changes need to be made
        else:
            return None

        return self.startTime

    def stop(self):
        """Change running state to stopped and return current elapsed time"""
        if self.mode == 'running':
            self.__elapsed_time()
            self.mode = 'stopped'
        # see line 22
        else:
            return None

    def reset(self):
        """"Change the running state to reset and clear counters"""
        if self.mode == 'running' or self.mode == 'stopped':
            self.mode = 'reset'
            self.startTime = 0
            self.elapsed = 0
        # see line 22
        else:
            return None

    def current_mode(self):
        """Return the current running mode of the clocker"""
        return self.mode

    def __elapsed_time(self):
        """updates or just returns the current elapsed time"""
        if self.mode == 'running':
            self.elapsed = time.time() - self.startTime
            return self.elapsed
        # if the clocker is any other state then no need to update
        # just return the current value of self.elapsed
        else:
            return self.elapsed

    def elapsed_seconds(self):
        """Return the current elapsed time in seconds"""
        if self.mode == 'running' or self.mode == 'stopped':
            return self._round_three_decimals(self.__elapsed_time())

        elif self.mode == 'reset':
            # when the mode is reset, no need to make any calculation
            # just return the current __elapsed_time which should always be 0
            return self.__elapsed_time()

        else:
            return None

    def elapsed_minutes(self):
        """Returns the current elapsed time in minutes"""
        if self.mode == 'running' or self.mode == 'stopped':
            return self._round_two_decimals(self.__elapsed_time()/60)

        elif self.mode == 'reset':
            # see line 67
            return self.__elapsed_time()

        else:
            return None

    def elapsed_hours(self):
        """Returns the current elapsed time in hours"""
        if self.mode == 'running' or self.mode == 'stopped':
            return self._round_two_decimals(self.__elapsed_time()/3600)

        elif self.mode == 'reset':
            # see line 67
            return self.__elapsed_time()

        else:
            return None

    def _round_two_decimals(self, float_number):
        """Take a floating point number and round it to two decimal places"""
        return math.ceil(float_number*100)/100

    def _round_three_decimals(self, float_number):
        """Take a floating point number and round it to two decimal places"""
        return math.ceil(float_number*1000)/1000
