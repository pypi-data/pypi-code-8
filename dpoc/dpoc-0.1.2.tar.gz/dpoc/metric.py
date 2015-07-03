import time
import json
import socket
import re
import make_json_serializable

class Metric():

    num_format = re.compile("^\-?\d+\.?\d*")
    str_format = re.compile("[^a-zA-Z0-9\./\-_]")

    def __init__(self, metric, value, **kwargs):
        self.metric = metric
        self.value = value
        self.timestamp = kwargs.pop("timestamp", int(time.time()))
        tags = {
            "host":socket.gethostname()
        }
        tags.update(kwargs)
        self.tags = tags
        self._sanitize()

    # Strip out all the characters that OpenTSDB forbids and makes sure we
    # have a numeric value
    #
    # http://opentsdb.net/docs/build/html/user_guide/writing.html
    #
    def _sanitize(self):
        self.metric = Metric.str_format.sub('-', self.metric)

        if not Metric.num_format.match(self.value.__repr__()):
            raise ValueError("Got non numeric data for metric value: %s" % self.value)

        sanitized_tags = {}
        for key, value in self.tags.iteritems():
            new_key = Metric.str_format.sub('-', key)
            new_value = Metric.str_format.sub('-', self.tags[key])
            # Skip if we replaced the entire key or value
            if new_key == len(new_key) * '-' or new_value == len(new_value) * '-':
                continue
            sanitized_tags[new_key] = new_value
        self.tags = sanitized_tags

    def __repr__(self):
        return json.dumps(self.__dict__)

    def to_json(self):
        return self.__dict__
