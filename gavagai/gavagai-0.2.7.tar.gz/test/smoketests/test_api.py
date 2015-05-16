#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
import json
import requests
import pytest
from gavagai.client import GavagaiClient

@pytest.fixture
def client(request):
    if not os.environ['GAVAGAI_APIKEY']:
        raise Exception('Environment variable GAVAGAI_APIKEY must be set.')
    return GavagaiClient()


def test_english_lexicon(client):
    r = client.lexicon('good')
    assert r.status_code == 200
    assert 'wordInformation' in r.json()


def test_swedish_lexicon(client):
    r = client.lexicon('jättebra', language='sv')
    assert r.status_code == 200
    assert 'wordInformation' in r.json()


def test_keywords(client):
    texts = get_swagger_json('texts', 'https://developer.gavagai.se/swagger/spec/keywords.json')
    r = client.keywords(texts)
    assert r.status_code == 200
    assert 'keywords' in r.json()
    assert len(r.json()['keywords']) > 0


def test_stories(client):
    texts = get_swagger_json('texts', 'https://developer.gavagai.se/swagger/spec/stories.json')
    r = client.stories(texts)
    assert r.status_code == 200
    assert 'stories' in r.json()
    assert len(r.json()['stories']) > 0


def test_tonality(client):
    texts = get_swagger_json('texts', 'https://developer.gavagai.se/swagger/spec/tonality.json')
    r = client.tonality(texts)
    assert r.status_code == 200
    assert 'texts' in r.json()
    assert len(r.json()['texts']) > 0


def test_topics(client):
    texts = get_swagger_json('texts', 'https://developer.gavagai.se/swagger/spec/topics.json')
    r = client.topics(texts)
    assert r.status_code == 200
    assert 'topics' in r.json()
    assert len(r.json()['topics']) > 0


def get_swagger_json(prop, url):
    res = requests.get(url)
    assert res.status_code == 200

    swagger = res.json()
    swagger_parameters = swagger['apis'][0]['operations'][0]['parameters']
    body_params = [p for p in swagger_parameters if p['paramType'] == 'body']
    sample_body = body_params[0]['defaultValue']
    
    result = json.loads(sample_body)[prop]
    assert isinstance(result, list)
    assert len(result) > 0
    return result
