import os
import pytest
from gavagai.client import GavagaiClient
from gavagai.exceptions import GavagaiException


def test_constructor_apikey():
    client = GavagaiClient('this_is_a_fake_apikey')
    assert client.apikey == 'this_is_a_fake_apikey'


def test_default_host():
    client = GavagaiClient('x')
    assert client.host == 'https://api.gavagai.se'


def test_default_api_version():
    client = GavagaiClient('x')
    assert client.api_version == 'v3'


def test_base_url():
    client = GavagaiClient('x')
    assert client.base_url() == 'https://api.gavagai.se/v3'


def test_custom_host():
    client = GavagaiClient('x', host='http://example.com')
    assert client.base_url() == 'http://example.com/v3'
    assert client.host == 'http://example.com'


def test_environment_variable():
    old_apikey = os.environ['GAVAGAI_APIKEY']
    os.environ['GAVAGAI_APIKEY'] = 'foo'
    client = GavagaiClient()
    assert client.apikey == 'foo'
    os.environ['GAVAGAI_APIKEY'] = old_apikey


def test_no_apikey():
    old_apikey = os.environ['GAVAGAI_APIKEY']
    del os.environ['GAVAGAI_APIKEY']
    with pytest.raises(GavagaiException):
        GavagaiClient()
    os.environ['GAVAGAI_APIKEY'] = old_apikey;


def test_request_kwargs():
    client = GavagaiClient('x', api_version='v5', default_option='foo')
    print(client.default_request_options)
    assert 'default_option' in client.default_request_options
