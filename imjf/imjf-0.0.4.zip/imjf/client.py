
import time
import re

import requests

from .exceptions import IMJFException

USER_AGENT = 'imjf-py'
API_DOMAIN_NAME = 'api.ismyjsfucked.com'
API_VERSION = 'v0'

def ismyjsfucked(urls, *args, **kw):
    """ This takes a list of URLs and determines if the JavaScript code is broken. Returning `True` indicates that at
        least one URL is confirmed for being broken. `None` indicates that at least one URL is unknown. `False`
        indicates everything is ok. An `IMJFException` will be raised if something goes wrong. """

    return report(urls, *args, **kw).get('fucked', None)

def report(urls, *args, **kw):
    """ This returns a detailed report for the URLs, or raises an `IMJFException`. """

    for status_code, report in _poll_reports(urls, *args, **kw):
        pass

    if _isnt_ok(status_code):
        raise IMJFException(report.get('message', 'Something went wrong'))
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

    make_request = getattr(requests, method.lower())

    try:
        response = make_request(url, json=data, headers={'User-Agent': USER_AGENT})
    except requests.RequestException:
        raise IMJFException('An error occurred while making a request to {api}'.format(api=API_DOMAIN_NAME))
    else:
        try:
            json_data = response.json()
        except ValueError:
            raise IMJFException("The response's JSON wasn't valid")
        else:
            return (response.status_code, json_data)

def _is_done(report):
    return report.get('status', 'done') == 'done'

def _isnt_ok(status_code):
    if status_code is None:
        return True
    else:
        return re.match(r'^2\d\d$', str(status_code)) is None

def _poll_reports(urls, use_status_code=True):

    url_params = '' if use_status_code else '?status-code=ignore'

    create_url = _api_url('reports') + url_params
    status_code, report = _request_json('POST', create_url, urls)

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

            get_url = _api_url('reports', str(report['id'])) + url_params
            status_code, report = _request_json('GET', get_url)
