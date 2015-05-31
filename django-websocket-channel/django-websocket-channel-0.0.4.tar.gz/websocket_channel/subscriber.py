# -*- coding: utf-8 -*-
from .web_socket_message import RedisStore


class RedisSubscriber(RedisStore):

    def __init__(self, connection):
        self._subscription = None
        super(RedisSubscriber, self).__init__(connection)

    def parse_response(self):
        """
        Parse a message response sent by the Redis datastore on a subscribed channel.
        """
        return self._subscription.parse_response()

    def set_pubsub_channels(self, request, channels):
        self._subscription = self._connection.pubsub()
        for channel in channels:
            self._subscription.subscribe(channel)

    def subscribe(self, channel):
        if self._subscription and channel not in self._subscription.channels:
            self._subscription.subscribe(channel)

    def send_persited_messages(self, websocket):
        """
        This method is called immediately after a websocket is openend by the client, so that
        persisted messages can be sent back to the client upon connection.
        """
        for channel in self._subscription.channels:
            message = self._connection.get(channel)
            if message:
                websocket.send(message)

    def get_file_descriptor(self):
        """
        Returns the file descriptor used for passing to the select call when listening
        on the message queue.
        """
        return self._subscription.connection and self._subscription.connection._sock.fileno()

    def release(self):
        """
        New implementation to free up Redis subscriptions when websockets close. This prevents
        memory sap when Redis Output Buffer and Output Lists build when websockets are abandoned.
        """
        if self._subscription and self._subscription.subscribed:
            self._subscription.unsubscribe()
            self._subscription.reset()

