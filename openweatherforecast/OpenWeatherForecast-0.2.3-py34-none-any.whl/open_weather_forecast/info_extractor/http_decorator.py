import time
from functools import wraps


def auto_tries(exception_to_catch, tries=4, delay=3):
    """
    Decorator to auto_tries the weather info

    :param tries:
    :param delay: Expressed in seconds, the waiting time between tries
    :return:
    """

    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            for internal_tries in range(tries):
                try:
                    return f(*args, **kwargs)
                except exception_to_catch:
                    print("Retrying in {} seconds".format(delay))
                    time.sleep(delay)
            return None

        return f_retry

    return deco_retry
