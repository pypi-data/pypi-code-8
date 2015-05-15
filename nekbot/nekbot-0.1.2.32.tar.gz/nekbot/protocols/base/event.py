__author__ = 'nekmo'


class Event(object):
    event_name = None
    def __init__(self, protocol, data=None):
        self.protocol = protocol
        self.data = data