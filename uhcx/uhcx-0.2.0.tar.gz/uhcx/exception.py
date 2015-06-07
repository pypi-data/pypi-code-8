# -*- coding: utf-8 -*-
"""
uh.cx API interface

http://uh.cx/
"""


class CouldNotConnectException(Exception):
    pass


class InvalidResponseException(Exception):
    pass


class CouldNotDecodeJsonException(Exception):
    pass