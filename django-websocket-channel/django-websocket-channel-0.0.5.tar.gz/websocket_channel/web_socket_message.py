# -*- coding: utf-8 -*-
import json
import six

class RedisMessage(six.binary_type):

    def __new__(cls, value):
        if isinstance(value, six.string_types):
            return six.binary_type.__new__(cls, value)
        elif isinstance(value, list):
            if len(value) >= 2 and value[0] == 'message':
                channel = value[1]
                return six.binary_type.__new__(cls, json.dumps({'channel': channel, 'content': value[2]}))
        return None


class RedisStore(object):
    """
    Abstract base class to control publishing and subscription for messages to and from the Redis
    datastore.
    """

    def __init__(self, connection):
        self._connection = connection
        self._publishers = set()

    def publish_message(self, message):

        if not isinstance(message, RedisMessage):
            message = RedisMessage(message)

        for channel in self._publishers:
            self._connection.publish(channel, message)
