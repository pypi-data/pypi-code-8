from agms.exception.agms_exception import AgmsException


class NotFoundException(AgmsException):
    """
    Raised when an object is not found in the gateway.
    """
    pass

