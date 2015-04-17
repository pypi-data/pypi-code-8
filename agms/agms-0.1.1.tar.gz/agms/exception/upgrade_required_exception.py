from agms.exception.agms_exception import AgmsException


class UpgradeRequiredException(AgmsException):
    """
    Raised for unsupported client library versions.
    """
    pass

