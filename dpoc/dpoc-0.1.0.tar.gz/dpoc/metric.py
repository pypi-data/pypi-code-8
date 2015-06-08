import time
import json
import socket
import make_json_serializable

class Metric():

    def __init__(self, metric, value, **kwargs):
        self.metric = metric
        self.value = value
        self.timestamp = kwargs.pop("timestamp", int(time.time()))
        tags = {
            "host":socket.gethostname()
        }
        tags.update(kwargs)
        self.tags = tags

    def __repr__(self):
        return json.dumps(self.__dict__)

    def to_json(self):
        return self.__dict__
