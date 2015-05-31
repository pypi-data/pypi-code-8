#-*- coding: utf-8 -*-
from redis import ConnectionPool, StrictRedis
from .ws_settings import WS_SETTINGS
from six import string_types
from .web_socket_message import RedisStore

redis_connection_pool = ConnectionPool(**WS_SETTINGS['WS_REDIS'])


class RedisPublisher(RedisStore):
    def __init__(self, publishers):
        """
        Initialize the channels for publishing messages through the message queue.
        """
        connection = StrictRedis(connection_pool=redis_connection_pool)
        super(RedisPublisher, self).__init__(connection)
        if isinstance(publishers, string_types):
            publishers = [publishers]
        self._publishers = publishers

