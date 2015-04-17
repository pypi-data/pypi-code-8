from agms.exception.agms_exception import AgmsException


class ForgedQueryStringException(AgmsException):
    """
    Raised when the query string has been forged or tampered with during a transparent redirect.
    """
    pass
