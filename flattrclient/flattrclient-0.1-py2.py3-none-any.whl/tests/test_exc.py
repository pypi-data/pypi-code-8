from pytest import raises
from flattrclient.exc import (raise_exception,
    FlattrApiError,
    InvalidRequestError,
    InvalidParametersError,
    UnauthorizedError,
    RateLimitExceededError,
    InvalidScopeError,
    InsufficientScopeError,
    NotFoundError,
    NotAccaptableError)

def test_raise_exception():
    with raises(InvalidRequestError):
        raise_exception(400, 'invalid_request', 'testing')

    with raises(InvalidParametersError):
        raise_exception(400, 'invalid_parameters', 'testing')

    with raises(UnauthorizedError):
        raise_exception(401, 'unauthorized', 'testing')

    with raises(RateLimitExceededError):
        raise_exception(403, 'rate_limit_exceeded', 'testing')

    with raises(InvalidScopeError):
        raise_exception(403, 'invalid_scope', 'testing')

    with raises(InsufficientScopeError):
        raise_exception(403, 'insufficient_scope', 'testing')

    with raises(NotFoundError):
        raise_exception(404, 'not_found', 'testing')

    with raises(NotAccaptableError):
        raise_exception(406, 'not_acceptable', 'testing')

    with raises(FlattrApiError):
        raise_exception(1, 'not_found', 'testing')

    with raises(FlattrApiError):
        raise_exception(404, 'testing', 'testing')
