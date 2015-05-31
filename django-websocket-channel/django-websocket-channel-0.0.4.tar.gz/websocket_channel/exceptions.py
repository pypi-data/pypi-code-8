#-*- coding: utf-8 -*-
from socket import error as socket_error
from django.http import BadHeaderError


class WebSocketError(socket_error):
    """
    WebSocket常规错误
    """


class FrameTooLargeException(WebSocketError):
    """
    Raised if a received frame is too large.
    """


class HandshakeError(BadHeaderError):
    """
    握手发生错误了
    """


class UpgradeRequiredError(HandshakeError):
    """
    Raised if protocol must be upgraded.
    """
