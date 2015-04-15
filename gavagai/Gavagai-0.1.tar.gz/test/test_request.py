import pytest
import httpretty
from requests import ConnectionError
from gavagai.client import GavagaiClient
from gavagai.exceptions import GavagaiHttpException


@httpretty.activate
def test_post_request():
    httpretty.register_uri(httpretty.POST, 'http://api.local/v3/test',
                           body='{"hello": "world"}', 
                           content_type='application/json')
    client = GavagaiClient('foo', host='http://api.local')
    response = client.request('/test', method='POST', body={'test':'value'})
    assert response.json() == {'hello': 'world'}
    assert httpretty.last_request().method == 'POST'
    assert httpretty.last_request().headers['content-type'] == 'application/json'
    assert httpretty.last_request().path == '/v3/test?apiKey=foo'


@httpretty.activate
def test_default_method_post():
    httpretty.register_uri(httpretty.POST, 'http://api.local/v3/test')
    client = GavagaiClient('foo', host='http://api.local')
    client.request('test')
    assert httpretty.last_request().method == 'POST'


@httpretty.activate
def test_path_with_slashes():
    httpretty.register_uri(httpretty.POST, 'http://api.local/v3/test')
    client = GavagaiClient('foo', host='http://api.local')
    path = '/test/'
    response = client.request(path)
    assert response.status_code == 200


@httpretty.activate
def test_empty_response():
    httpretty.register_uri(httpretty.GET, 'http://api.local/v3/test', status=204)
    client = GavagaiClient('foo', host='http://api.local')
    response = client.request('test', method='get')
    assert response.status_code == 204


@httpretty.activate
def test_raise_exception_on_300_range_status():
    httpretty.register_uri(httpretty.GET, 'http://api.local/v3/test', status=302)
    client = GavagaiClient('foo', host='http://api.local')
    with pytest.raises(GavagaiHttpException) as excinfo:
        client.request('test', method='get')
    assert excinfo.value.status_code == 302


@httpretty.activate
def test_raise_exception_on_400_range_status():
    httpretty.register_uri(httpretty.GET, 'http://api.local/v3/test', status=401, 
                           body='{"message": "fake api error message"}',
                           content_type='application/json')

    client = GavagaiClient('foo', host='http://api.local')
    with pytest.raises(GavagaiHttpException) as excinfo:
        client.request('test', method='get')
    assert excinfo.value.message == '{"message": "fake api error message"}'
    assert excinfo.value.status_code == 401


@httpretty.activate
def test_raise_exception_on_500_range_status():
    httpretty.register_uri(httpretty.GET, 'http://api.local/v3/test', status=502, 
                           body='Fake bad gateway error',
                           content_type='text/plain')

    client = GavagaiClient('foo', host='http://api.local')
    with pytest.raises(GavagaiHttpException) as excinfo:
        client.request('test', method='get')
    assert excinfo.value.status_code == 502
    assert excinfo.value.message == 'Fake bad gateway error'


@httpretty.activate
def test_default_exception_message_if_empty_error_message_from_api():
    httpretty.register_uri(httpretty.GET, 'http://api.local/v3/test', status=500, body=None)
    client = GavagaiClient('foo', host='http://api.local')
    with pytest.raises(GavagaiHttpException) as excinfo:
        client.request('test', method='get')
    assert excinfo.value.status_code == 500
    assert 'Unable to complete HTTP request' in excinfo.value.message


@httpretty.activate
def test_connection_error_exception_on_host_unreachable():
    client = GavagaiClient('x', host='http://unreachablehost')
    with pytest.raises(ConnectionError):
        client.request('test', method='get')


