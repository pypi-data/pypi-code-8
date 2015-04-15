import re
import six
import types
import functools
import requests
from simplejson.decoder import JSONDecodeError
from flattrclient.exc import raise_exception

def _handle_response(resp, accepted_codes=[200], do_json=True):
    if resp is None:
        # If there is no response, most likely because no request happened,
        # just also return None.
        return resp
    if resp.status_code not in accepted_codes:
        try:
            res = resp.json()
            error = res['error']
            description = res['error_description']
        except JSONDecodeError:
            # just a hack, since 404 could come without json-body
            error = 'not_found'
            description = resp.text
        raise_exception(resp.status_code, error, description)
    if resp.status_code != 204:
        return resp.json()
    return ''


def result(cls):
    def _result(fn):
        @functools.wraps(fn)
        def __result(self, *args, **kwargs):
            resp = fn(self, *args, **kwargs)
            res = _handle_response(resp)
            if res is None:
                return None
            elif isinstance(res, list):
                return (cls(session=self._session, dirty=False, **elm) for elm in res)
            else:
                return cls(session=self._session, dirty=False, **res)
        return __result
    return _result

def _replace_(ob, parts):
    """Repaces parts by object values
    >>> class A(object):
    ...     _username = 'my'
    ...     _testing = 'test'
    >>> '/'.join(_replace_(A(), ['this', ':username', 'is', ':testing', 'stuff']))
    'this/my/is/test/stuff'
    """
    for part in parts:
        if part.startswith(':'):
            yield str(getattr(ob, '_%s' % part[1:]))
        else:
            yield part

def _api_call(map_url, method='get', additional_params={},
        additional_headers={}):
    def __api_call(fn):
        @functools.wraps(fn)
        def ___api_call(self, *args, **kwargs):
            params = fn(self, *args, **kwargs)
            if params == False:
                # If params is False, no request should happen.
                # e.g. if the thing is not dirty, it should not be updated,
                # do save some api-calls.
                # Return None to indicate further decorators about no request.
                return None
            if ':' in map_url:
                _map_url = '/'.join(_replace_(self, map_url.split('/')))
            else:
                _map_url = map_url
            url = '%s%s' % (self._get_url(), _map_url)
            q = {}
            if isinstance(params, six.string_types):
                if url.endswith('/'):
                    url += params
                else:
                    url += '/' + params
            else:
                q = params
                if additional_params:
                    q.update(additional_params)
            req_fn = getattr(self._session, method)
            if method in ('post', 'patch', 'put'):
                # On posting style method, the field called data instead of
                # params.
                do_request = functools.partial(req_fn, url, data=q)
            else:
                do_request = functools.partial(req_fn, url, params=q)
            if additional_headers:
                # If there are additional headers for one special request
                headers = self._session.headers
                headers.update(additional_headers)
                return do_request(headers=headers)
            return do_request()
        return ___api_call
    return __api_call

def get(map_url, additional_headers={}):
    """ GET request to flattr api """
    return _api_call(map_url, additional_headers=additional_headers)

def post(map_url, additional_headers={}):
    """ POST request to flattr api """
    return _api_call(map_url, method='post',
            additional_headers=additional_headers)

def put(map_url, additional_headers={}):
    """ PUT request to flattr api """
    return _api_call(map_url, method='put',
            additional_headers=additional_headers)

def patch(map_url, additional_headers={}):
    """ PATCH request to flattr api.

    due to a problem at flattrs api, patch must be post with the additional
    parameter _method set to patch:
    http://developers.flattr.net/api/resources/things/#update-a-thing
    """
    return _api_call(map_url, method='post',
            additional_params={'_method': 'patch'},
            additional_headers=additional_headers)

def delete(map_url, additional_headers={}):
    """ DELETE request to flattr api. """
    return _api_call(map_url, method='delete',
        additional_headers=additional_headers)

def refresh_thing_id(fn):
    """ Returns the json result and sets the fields:
       _id to new id
       _dirty to False
    """
    @functools.wraps(fn)
    def _refresh_thing_id(self, *args, **kwargs):
        resp = fn(self, *args, **kwargs)
        res = _handle_response(resp, accepted_codes=[201])
        if res is None:
            return None
        if 'id' in res:
            self._id = int(res['id'])
            self._dirty = False
        return res
    return _refresh_thing_id

def just_json(param):
    """ Decorator to just return json from request.
    You can use it in two ways.
    First, just passing the function:
       @flattrclient.just_json
       @flattrclient.get('/blah')
       def test():
           return {}
    This accepts status_code 200 and returns a json.

    You can also pass a list of accepted_status codes and the function:
       @flattrclient.just_json([201, 204])
       @flattrclient.get('/blah')
       def test():
           return {}
    Now, status_codes 201 and 204 are accepted and the json is returned.
    """
    def _just_json(accepted_codes):
        def __just_json(fn):
            @functools.wraps(fn)
            def ___just_json(self, *args, **kwargs):
                resp = fn(self, *args, **kwargs)
                res = _handle_response(resp, accepted_codes=accepted_codes)
                if res is None:
                    return None
                return res
            return ___just_json
        return __just_json
    # Some black magick. If param is a function, we accept status_code 200
    # _and_ we pass param as a function to __just_json
    #
    # If param is not a function. Only _just_json will be called and
    # __just_json is returned.
    if isinstance(param, types.FunctionType):
        return _just_json([200])(param)
    return _just_json(param)

def _get_query_dict(**kwargs):
    """Returns query dict by kwargs.
    Skip None-values, but keeps False etc.
    >>> res = _get_query_dict(url=None, test='a', page=True, full=False)
    >>> res == {'test': 'a', 'page': True, 'full': False}
    True
    """
    def __get_quey_dict(**kwargs):
        for k, v in six.iteritems(kwargs):
            if v is not None:
                yield k, v
    return dict(__get_quey_dict(**kwargs))
