#!/usr/bin/python
# -*- coding: utf-8 -*-

from gavagai.client import GavagaiClient
from pprint import pprint

texts = [u'Din idiot!', u'Jag älskar dig.', u'Hen hatar det.']

client = GavagaiClient() # get your own apikey at https://developer.gavagai.se
data = client.tonality(texts, language='sv').json()

pprint(data)