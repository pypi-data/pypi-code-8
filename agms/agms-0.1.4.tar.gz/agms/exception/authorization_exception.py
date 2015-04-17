from agms.exception.agms_exception import AgmsException


class AuthorizationException(AgmsException):
    """
    Raised when the user does not have permission to complete the requested operation.
    """
    pass