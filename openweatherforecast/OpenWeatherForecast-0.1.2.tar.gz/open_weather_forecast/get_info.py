from abc import ABCMeta
from functools import wraps
import time


class GetInfo(metaclass=ABCMeta):
    """
    Abstract class to retrieve information from a Json API
    """
    pass

    def filter_information(self, info_retrieved, schema, result=None):
        """
        :param info_retrieved: Info retrieved from the API
        :param schema: Schema defined by the user to extract partial information
        :param result: Structure containing the filtered information from the API
        :return:
        """
        if result is None:
            result = dict()

        for key in schema:
            if isinstance(info_retrieved, dict):
                value = info_retrieved.get(key, {})
            else:
                for element, sub_info in zip(info_retrieved, schema*len(info_retrieved)):
                    result.append(type(element)())
                    self.filter_information(element, sub_info, result[-1])
                continue

            info_type = type(schema.get(key)) if isinstance(schema.get(key), (list, dict)) else schema.get(key)
            if info_type is not type(value):
                msg = "Types from information schema and the information retrieved does not match {} {}"
                raise ValueError(msg.format(type(schema.get(key)), type(value)))

            if isinstance(value, (list, dict)):
                result[key] = type(value)()
                self.filter_information(info_retrieved.get(key), schema.get(key), result.get(key))
            else:
                if isinstance(result.get(key, None), list):
                    result[key].append(value)
                else:
                    result[key] = value
        return result

    @staticmethod
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
                        time.sleep(delay)
                return None

            return f_retry

        return deco_retry