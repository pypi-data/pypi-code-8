import os
import json
import pytest
import httpretty
from gavagai.client import GavagaiClient


@pytest.fixture
def client(request):
    dir = os.path.dirname(__file__)
    with open(os.path.join(dir, 'data/tonality_response.json')) as json_file:
        data = json_file.read()

    httpretty.enable()
    httpretty.register_uri(httpretty.POST, 'http://api.local/v3/tonality',
                           body=data, 
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
    client.tonality(texts)
    request = httpretty.last_request()
    assert '"language": "en"' in request.body


def test_input_list_of_text_objects(client, texts):
    client.tonality(texts)
    request_body = json.loads(httpretty.last_request().body)
    text_objects = request_body['texts']
    assert isinstance(text_objects, list)
    assert 'id' in text_objects[0]
    assert 'body' in text_objects[0]


def test_input_list_of_strings(client):
    client.tonality(['this is a text', 'this is text 2', 'this is the third text'])
    request_body = json.loads(httpretty.last_request().body)
    assert request_body['texts'][2]['body'] == 'this is the third text'


def test_custom_options_as_arguments(client, texts):
    client.tonality(texts, language='sv', myCustomOption='optionally optional')    
    request_body = json.loads(httpretty.last_request().body)
    assert request_body['language'] == 'sv'
    assert request_body['myCustomOption'] == 'optionally optional' 


def test_custom_options_as_dictionary(client, texts):
    options = {
        'anotherOption': 4711,
        'language': 'no'
    }
    client.tonality(texts, **options)    
    request_body = json.loads(httpretty.last_request().body)
    assert request_body['language'] == 'no'
    assert request_body['anotherOption'] == 4711


def test_throw_if_texts_argument_not_a_list(client):
    with pytest.raises(ValueError):
        client.tonality('this is not a list')


def test_return_tonality_dictionary_json_from_response(client):
    """Tonality for each text mapped into a dictionary instead of array"""
    response = client.tonality(['dummy text'])
    texts = response.simple_list()
    assert isinstance(texts, list)
    assert len(texts) == 10
    tonality = texts[0]['tonality']
    assert tonality['positivity']['score'] == 9
    assert tonality['positivity']['normalized_score'] == 0.75
    assert tonality.keys() == ['desire', 'love', 'positivity', 'violence', 
                               'skepticism', 'hate', 'fear', 'negativity']


