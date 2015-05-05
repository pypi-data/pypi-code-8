import urllib2
from threading import Thread

class Dispatcher(object):
    def __init__(self):
        self._map = {}

    def subscribe(self, channel, callback):
        if channel not in self._map:
            self._map[channel] = []
        self._map[channel].append(callback)

    def publish(self, channel, **kwargs):
        t = Thread(target=self._publish, args=(channel,), kwargs=kwargs)
        t.start()
        t.join()

    def _publish(self, channel, **kwargs):
        if channel in self._map:
            for callback in self._map[channel]:
                if isinstance(callback, basestring):
                    self.post_to_url(callback, **kwargs)
                elif callable(callback):
                    callback(**kwargs)

    def unsubscribe(self, channel, callback):
        if channel in self._map:
            if callback in self._map[channel]:
                self._map[channel].remove(callback)
    
    def post_to_url(self, url, **kwargs):
        urllib2.urlopen(url, data=str(kwargs))
