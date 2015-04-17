from agms.exception.agms_exception import AgmsException


class InvalidRequestException(AgmsException):
    """
    Raised a method cannot complete due to an invalid request to an API, called from the API object.
    """
    pass