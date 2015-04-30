#!/usr/bin/env python
'''Alpine/Chorus Client API Module'''

import logging
import requests

LOG = logging.Logger(name=__name__)

CONTENT_TYPE = 'application/x-www-form-urlencoded'
JSON_CONTENT_TYPE = 'application/json'

def get(url, session):
    '''Perform GET request using current session'''
    isok, json, cookies = _perform_http_method_(
        session.config.get('alpine', 'host'),
        _get_(url, session.sid, session.cookies))
    session.cookies = cookies
    return (isok, json,)

def post(url, session, data=None):
    '''Perform POST request using current session'''
    isok, json, cookies = _perform_http_method_(
        session.config.get('alpine', 'host'),
        _post_(url, session.sid, session.cookies, data=data))
    session.cookies = cookies
    return (isok, json,)

def put(url, session, data=None):
    '''Perform PUT request using current session'''
    isok, json, cookies = _perform_http_method_(
        session.config.get('alpine', 'host'),
        _put_(url, session.sid, session.cookies, data=data))
    session.cookies = cookies
    return (isok, json,)

def delete(url, session):
    '''Perform DELETE request using current session'''
    isok, json, cookies = _perform_http_method_(
        session.config.get('alpine', 'host'),
        _delete_(url, session.sid, session.cookies))
    session.cookies = cookies
    return (isok, json,)

def _get_url_(host, endpoint=""):
    '''Return the host and path for the chorus instance'''
    return "http://%s/%s" % (host, endpoint)

def _perform_http_method_(host, request_data):
    '''Perform IO operation to Chorus Server using request_data object'''
    methods = {'GET': requests.get,
               'POST': requests.post,
               'PUT': requests.put,
               'DELETE': requests.delete,}
    method = methods[request_data['method']]
    response = method(_get_url_(host, request_data['url']),
                      params=request_data['params'],
                      headers=request_data['headers'],
                      cookies=request_data['cookies'],
                      data=request_data['data'])
    LOG.info("Request: %s status code: %d",
             request_data['url'],
             response.status_code)
    return (response.status_code, response.json(), dict(response.cookies),)

def _get_(url, sid, cookies):
    '''Create GET request data'''
    return {
        'data': None,
        'params': {
            'session_id': sid,
        },
        'headers': {
            'content-type': CONTENT_TYPE,
        },
        'cookies': cookies,
        'url': url,
        'method': 'GET',
    }

def _post_(url, sid, cookies, data):
    '''Create POST request data'''
    return {
        'data': data,
        'params': {
            'session_id': sid,
        },
        'headers': {
            'content-type': CONTENT_TYPE,
        },
        'cookies': cookies,
        'url': url,
        'method': 'POST',
    }

def _put_(url, sid, cookies, data):
    '''Create PUT request data'''
    return {
        'data': data,
        'params': {
            'session_id': sid,
        },
        'headers': {
            'content-type': CONTENT_TYPE,
        },
        'cookies': cookies,
        'url': url,
        'method': 'PUT',
    }

def _delete_(url, sid, cookies):
    '''Create DELETE request data'''
    return {
        'data': None,
        'params': {
            'session_id': sid,
        },
        'headers': {
            'content-type': CONTENT_TYPE,
        },
        'cookies': cookies,
        'url': url,
        'method': 'DELETE',
    }
