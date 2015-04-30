#!/usr/bin/env python
'''Chorus Client Test Cases'''

import logging
from pylibchorus.chorus_api import _get_
from pylibchorus.chorus_api import _post_
from pylibchorus.chorus_api import _put_
from pylibchorus.chorus_api import _delete_
import sys
if sys.version_info[0] == 2 and sys.version_info[1] == 6:
    import unittest2 as unittest
else:
    import unittest

LOG = logging.getLogger(__name__)

def check_request_structure(testcase, request_obj):
    '''Test the request structure is correct'''
    testcase.assertIsNotNone(request_obj)
    testcase.assertIn('data', request_obj)
    testcase.assertIn('headers', request_obj)
    testcase.assertIn('params', request_obj)
    testcase.assertIn('cookies', request_obj)
    testcase.assertIn('url', request_obj)
    testcase.assertIn('method', request_obj)
    check_header(testcase, request_obj['headers'])

def check_header(testcase, header):
    '''Test the header object conforms to the what the API requires'''
    testcase.assertIsNotNone(header)
    testcase.assertIn('content-type', header)
    testcase.assertEquals(header['content-type'],
                          'application/x-www-form-urlencoded')

def check_params(testcase, params, expected_sid):
    '''Check the params object contains the correct session_id'''
    testcase.assertIsNotNone(params)
    testcase.assertIn('session_id', params)
    testcase.assertEqual(params['session_id'], expected_sid)

class ChorusSessionTests(unittest.TestCase):
    '''ChorusSession Test Case'''

    def test_get_returns_request_data(self):
        '''Test _get_ returns correct request data'''
        url = '/'
        sid = 'foobar'
        cookies = {'session_id': sid}
        actual = _get_(url, sid, cookies)
        check_request_structure(self, actual)
        check_params(self, actual['params'], sid)
        self.assertIsNone(actual['data'])
        self.assertEquals(url, actual['url'])
        self.assertEquals('GET', actual['method'])

    def test_post_returns_request_data(self):
        '''Test _post_ returns correct request data'''
        url = '/workfiles/42'
        sid = 'foobar'
        cookies = {'session_id': sid}
        post_data = {'foo': 'bar'}
        actual = _post_(url, sid, cookies, data=post_data)
        check_request_structure(self, actual)
        check_params(self, actual['params'], sid)
        self.assertIsNotNone(actual['data'])
        self.assertIn('foo', actual['data'])
        self.assertEquals('bar', actual['data']['foo'])
        self.assertEquals(url, actual['url'])
        self.assertEquals('POST', actual['method'])

    def test_put_returns_request_data(self):
        '''Test _put_ returns correct request data'''
        url = '/workfiles/42/version/0'
        sid = 'foobar'
        cookies = {'session_id': sid}
        put_data = {'foo': 'bar'}
        actual = _put_(url, sid, cookies, data=put_data)
        check_request_structure(self, actual)
        check_params(self, actual['params'], sid)
        self.assertIsNotNone(actual['data'])
        self.assertIn('foo', actual['data'])
        self.assertEquals('bar', actual['data']['foo'])
        self.assertEquals(url, actual['url'])
        self.assertEquals('PUT', actual['method'])

    #pylint: disable=C0103
    def test_delete_returns_request_data(self):
        '''Test _delete_ returns correct request data'''
        url = '/workfiles/42/versions/0'
        sid = 'foobar'
        cookies = {'session_id': sid}
        actual = _delete_(url, sid, cookies)
        check_request_structure(self, actual)
        self.assertIsNone(actual['data'])
        check_params(self, actual['params'], sid)
