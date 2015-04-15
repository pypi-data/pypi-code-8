import os
import json
import pytest
import httpretty
from gavagai.client import GavagaiClient


@pytest.fixture
def client(request):
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, 'http://api.local/v3/stories',
                           body='{"foo": "bar"}', 
                           content_type='application/json')
    def client_teardown():
        httpretty.disable()
        httpretty.reset()
    request.addfinalizer(client_teardown)    
    return GavagaiClient('foo', host='http://api.local')


@pytest.fixture
def texts():
    dir = os.path.dirname(__file__)
    with open(os.path.join(dir, 'data/texts.json')) as json_file:
        texts = json.load(json_file)
    return texts


def test_default_language(client, texts):
    client.stories(texts)
    request = httpretty.last_request()
    assert '"language": "en"' in request.body


def test_input_list_of_text_objects(client, texts):
    client.stories(texts)
    body = json.loads(httpretty.last_request().body)
    text_objects = body['texts']
    assert isinstance(text_objects, list)
    assert 'id' in text_objects[0]
    assert 'body' in text_objects[0]


def test_input_list_of_strings(client):
    client.stories(['this is a text', 'this is text 2', 'this is the third text'])
    body = json.loads(httpretty.last_request().body)
    assert body['texts'][2]['body'] == 'this is the third text'


def test_custom_options_as_arguments(client, texts):
    client.stories(texts, language='sv', myCustomOption='optionally optional')    
    body = json.loads(httpretty.last_request().body)
    assert body['language'] == 'sv'
    assert body['myCustomOption'] == 'optionally optional' 


def test_custom_options_as_dictionary(client, texts):
    options = {
        'anotherOption': 4711,
        'language': 'no'
    }
    client.stories(texts, **options)    
    body = json.loads(httpretty.last_request().body)
    assert body['language'] == 'no'
    assert body['anotherOption'] == 4711


def test_throw_if_texts_argument_not_a_list(client):
    with pytest.raises(ValueError):
        client.stories('this is not a list')
