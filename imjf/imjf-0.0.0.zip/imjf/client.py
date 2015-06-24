
import time

import requests

from .exceptions import IMJFException

API_DOMAIN_NAME = 'api.ismyjsfucked.com'
API_VERSION = 'v0'

def is_my_js_fucked(*urls):
    """ Takes URLs and determines if their JavaScript code is broken. Returning `True` indicates that at least one
        URL is confirmed for being broken. `None` indicates that at least one URL is unknown. `False` indicates
        everything is ok. An `IMJFException` will be raised if something goes wrong. """

    return report(*urls).get('fucked', None)

def report(*urls):
    """ This returns a detailed report for the URLs, or raises an `IMJFException`. """

    for status_code, report in _poll_reports(*urls):
        pass

    if _isnt_ok(status_code):
        raise IMJFException(report.get('message', ''))
    else:
        return report

def _api_url(*path):
    url = 'http://{domain_name}/{version}/'.format(domain_name=API_DOMAIN_NAME, version=API_VERSION)
    if path:
        return url + '/'.join(path) + '/'
    else:
        return url

def _request_json(method, url, data=None):
    assert method.lower() in {'post', 'get'}

    try:
        response = getattr(requests, method.lower())(url, json=data)
    except requests.RequestException:
        raise IMJFException()
    else:
        try:
            json_data = response.json()
        except ValueError:
            raise IMJFException()
        else:
            return (response.status_code, json_data)

def _is_done(report):
    return report.get('status', 'done') == 'done'

def _isnt_ok(status_code):
    return not str(status_code).startswith('2')

def _poll_reports(*urls):
    status_code, report = _request_json('POST', _api_url('reports'), urls)

    try:
        range_ = xrange
    except NameError:
        range_ = range

    for _ in range_(60 * 5):
        yield (status_code, report)

        if _is_done(report) or _isnt_ok(status_code):
            break
        else:
            time.sleep(1)
            status_code, report = _request_json('GET', _api_url('reports', str(report['id'])))
