import threading
from nekbot.core import events

__author__ = 'nekmo'


class Protocol(threading.Thread):
    features = []

    def __init__(self, nekbot):
        self.nekbot = nekbot
        threading.Thread.__init__(self)
        self.name = self.__class__.__name__.lower()
        self.daemon = True

        self.init()

    def prepare_message(self, body):
        if not isinstance(body, (str, unicode)):
            body = str(body)
        return body

    def propagate(self, event, *args, **kwargs):
        events.propagate(event, self, *args, **kwargs)

    def close(self):
        pass