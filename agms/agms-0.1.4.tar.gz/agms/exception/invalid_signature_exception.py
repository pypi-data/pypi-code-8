from agms.exception.agms_exception import AgmsException


class InvalidSignatureException(AgmsException):
    """
    Raised a method cannot complete due to an invalid signature of API, called from the API object.
    """
    pass
