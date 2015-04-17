from agms.exception.agms_exception import AgmsException


class ResponseException(AgmsException):
    """
    Raised when the request was successful but the server returned an error or failure message.
    """
    pass

