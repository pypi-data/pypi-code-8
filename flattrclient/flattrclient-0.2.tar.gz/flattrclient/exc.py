class FlattrApiError(Exception):
    """Generic flattr api error.
    For special errors have a look at:
    http://developers.flattr.net/api/#client-errors
    """
    pass

class InvalidRequestError(FlattrApiError):
    pass

class InvalidParametersError(FlattrApiError):
    pass

class UnauthorizedError(FlattrApiError):
    pass

class RateLimitExceededError(FlattrApiError):
    pass

class InvalidScopeError(FlattrApiError):
    pass

class InsufficientScopeError(FlattrApiError):
    pass

class NotFoundError(FlattrApiError):
    pass

class NotAccaptableError(FlattrApiError):
    pass

code_exception_mapping = {
    400: {'invalid_request': InvalidRequestError,
          'invalid_parameters': InvalidParametersError,
    },
    401: {'unauthorized': UnauthorizedError,},
    403: {'rate_limit_exceeded': RateLimitExceededError,
          'invalid_scope': InvalidScopeError,
          'insufficient_scope': InsufficientScopeError,
    },
    404: {'not_found': NotFoundError,},
    406: {'not_acceptable': NotAccaptableError,},
    }

def raise_exception(status_code, error, description):
    try:
        raise code_exception_mapping[status_code][error](description)
    except KeyError:
        raise FlattrApiError(description)
