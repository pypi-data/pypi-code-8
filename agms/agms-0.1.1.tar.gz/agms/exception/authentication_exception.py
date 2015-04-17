from agms.exception.agms_exception import AgmsException


class AuthenticationException(AgmsException):
    """
    Raised when the client library cannot authenticate with the gateway.  
    This generally means the username/password key are incorrect, or the merchant is not active.
    """
    pass
