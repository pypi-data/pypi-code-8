class ApiException(Exception):
    """
    Api exception.

    raised when kong api return status: False
        in response
    """
    pass


class NullResponseException(Exception):
    """
    Request returned blank line.
    """
    pass
