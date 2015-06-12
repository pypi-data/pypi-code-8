'''

@author: eh14
'''
import datetime
import time


class TimeProvider(object):
    """
    Small service providing access to time-related functions. Main intensive to have a service
    like this is the flexibility to replace it for testing.
    """
    def _now(self):
        return time.time()
    
    def now(self, integer=False):
        if integer:
            return int(round(self._now()))
        else:
            return self._now()
    
    def future(self, seconds, integer=False):
        ft = self.now() + seconds
        
        if integer:
            return int(round(ft))
        else:
            return ft
    
    def nowDate(self):
        return datetime.datetime.fromtimestamp(self._now())
    
    def futureDate(self, seconds):
        return datetime.datetime.fromtimestamp(self.future(seconds))