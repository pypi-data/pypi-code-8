# encoding: utf-8

from redis import StrictRedis
from redis.exceptions import RedisError
from datetime import datetime
import warnings
import logging
import socket
import time


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Graphite(object):
    def __init__(self, host='localhost', port=2003, prefix=''):
        self.socket = socket.socket()
        self.socket.connect((host, port))
        self.prefix = 'event_tracker.'
        if prefix:
            self.prefix += prefix + '.'

    def send_metric(self, metric_name, msg):
        metric_name = self.prefix + metric_name
        message = '%s %s %d\n' % (metric_name, msg, int(time.time()))
        self.socket.sendall(message)


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class EventTracker(Singleton):
    _redis = None

    def __init__(self, redis=None, host='localhost', port=6379, db=0, graphite_host=None, graphite_port=2003,
                 graphite_prefix=''):
        self.set_connection_to_redis(redis or self.get_connection_to_redis(host=host, port=port, db=db))
        self.graphite_host = graphite_host
        self.graphite_port = graphite_port
        self.graphite = None
        if graphite_host:
            try:
                self.graphite = Graphite(graphite_host, graphite_port, graphite_prefix)
            except Exception as e:
                msg = u"could not connect to graphite server: %s" % unicode(e)
                warnings.warn(msg)
                logger.warning(msg)

    @staticmethod
    def get_connection_to_redis(**kwargs):
        return StrictRedis(**kwargs)

    def set_connection_to_redis(self, redis):
        self._redis = redis

    def track_event(self, event_hash_name):
        date = datetime.now().date()
        try:
            if not self._redis.sismember('dates', date):
                self._redis.sadd('dates', date)
            total = self._redis.hincrby(event_hash_name, date, 1)

            if self.graphite:
                self.graphite.send_metric(event_hash_name, total)

        except RedisError as e:
            warnings.warn(unicode(e))
            logger.warning(u'{0}; event: {1}'.format(unicode(e), event_hash_name))
