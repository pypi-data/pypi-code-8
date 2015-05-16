from __future__ import absolute_import
import pytest
import httpretty
from gavagai.client import GavagaiClient


@pytest.fixture
def client(request):
    httpretty.enable()
    def client_teardown():
        httpretty.disable()
        httpretty.reset()
    request.addfinalizer(client_teardown)    
    return GavagaiClient('foo', host='http://api.local')


def test_single_word_default_language(client):
    httpretty.register_uri(httpretty.GET, 'http://api.local/v3/lexicon/en/foo')
    response = client.lexicon('foo')
    assert(response.status_code == 200)


def test_single_word_specified_language(client):
    httpretty.register_uri(httpretty.GET, 'http://api.local/v3/lexicon/sv/foo')
    response = client.lexicon('foo', language='sv')
    assert(response.status_code == 200)


def test_sequence_of_words(client):
    httpretty.register_uri(httpretty.GET, 'http://api.local/v3/lexicon/en/foo%20bar')
    response = client.lexicon('foo bar')
    assert(response.status_code == 200)


def test_throw_if_texts_argument_not_a_string(client):
    httpretty.register_uri(httpretty.GET, 'http://api.local/v3/lexicon/en/foo')
    with pytest.raises(ValueError):
        client.lexicon({})
