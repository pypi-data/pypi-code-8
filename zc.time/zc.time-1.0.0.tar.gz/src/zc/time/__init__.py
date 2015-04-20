import datetime
import pytz
import time


def now():
    if _t:
        return _t
    else:
        return datetime.datetime.now(pytz.UTC)


_now = now
_t = None


def utcnow():
    return now().replace(tzinfo=None)


def set_now(t):
    global _t
    tz = t.tzinfo
    if tz is None:
        t = pytz.UTC.localize(t)
    elif tz is not pytz.UTC:
        t = t.astimezone(pytz.UTC)
    time.sleep = _sleep
    time.time = _time
    _t = t


def reset():
    global now, _t
    now = _now
    _t = None
    time.sleep = _time_sleep
    time.time = _time_time


def _sleep(seconds):
    global _t
    if _t is None:
        # We shouldn't be involved; get out of the way:
        time.sleep = _time_sleep
        _time_sleep(seconds)
    else:
        td = datetime.timedelta(seconds=seconds)
        _time_sleep(seconds)
        _t += td


def _time():
    if _t is None:
        # We shouldn't be involved; get out of the way:
        time.time = _time_time
        return _time_time()
    else:
        return time.mktime(_t.timetuple()) + (_t.microsecond / 1000000.0)
    

_time_sleep = time.sleep
_time_time = time.time


# Play the conditional import game to avoid a required dependency.
try:
    import zope.testing.cleanup
except ImportError:
    pass
else:
    zope.testing.cleanup.addCleanUp(reset)
