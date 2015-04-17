from agms.exception.agms_exception import AgmsException


class RequestValidationException(AgmsException):
    """
    Raised when attempt to validate an API request fails from a function performing validation.
    """
    pass
