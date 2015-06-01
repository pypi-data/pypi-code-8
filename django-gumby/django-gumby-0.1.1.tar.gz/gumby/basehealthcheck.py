import time

class BaseHealthCheck(object):
    status = None
    extras = {}
    __response = None
    __start = None
    __end = None
    __secs = None
    __msecs = None

    def __init__(self):
        self.__start()
        self.check_status()
        self.__end()

    def __start(self):
        self.__start = time.time()
        return self

    def __end(self, *args):
        self.__end = time.time()
        self.__secs = self.__end - self.__start
        self.__msecs = self.__secs * 1000  # millisecs

    def check_status(self):
        return None

    def get_response(self):
        __response = {
            'identifier': self.identifier(),
            'elapsed': self.__msecs,
            'status': self.status,
        }
        if self.extras is not None:
            __response.update(self.extras)

        return __response

    @classmethod
    def identifier(cls):
        return cls.__name__
