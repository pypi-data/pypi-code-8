import ctypes

import pystormlib.winerror


def raise_for_error(func, *args, **kwargs):
    """Small helper around GetLastError

    :param func: a function using SetLastError internally
    :type func: callable
    :param args: Arbitrary Argument Lists
    :param kwargs: Keyword Arguments
    :return: func result
    :raise: PyStormException in case something when wrong with stormlib
    """
    ctypes.windll.kernel32.SetLastError(0)
    result = func(*args, **kwargs)
    error_code = ctypes.windll.kernel32.GetLastError()
    if error_code:
        exception = pystormlib.winerror.exceptions.get(
            error_code, pystormlib.winerror.exceptions
        )
        raise exception(error_code)
    return result