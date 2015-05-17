"""Module for warmama exceptions"""


class WarmamaException(Exception):
    """Base class for Warmama exceptions

    Attributes:
        status (int): Response status a view should return if this exception
            is encountered.
    """
    status = 500


class BadRequest(WarmamaException):
    """Exception raised for invalid form data or otherwise 400 responses"""
    status = 400


class Forbidden(WarmamaException):
    """Exception raised on authentication or permission failure"""
    status = 403
