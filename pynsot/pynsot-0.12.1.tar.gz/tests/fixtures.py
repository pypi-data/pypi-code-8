#!/usr/bin/env python

"""
Make dummy data and fixtures and stuff.
"""

import faker
import hashlib
import pytest
import random
import tempfile

from pynsot import client
from pynsot import dotfile

# Constants and stuff
fake = faker.Factory.create()

# Dummy config data used for testing dotfile and client
CONFIG_DATA = {
    'email': 'jathan@localhost',
    # 'url': 'http://localhost:8990/api',
    'url': 'http://localhost:8991/api',
    'auth_method': 'auth_token',
    'secret_key': 'MJMOl9W7jqQK3h-quiUR-cSUeuyDRhbn2ca5E31sH_I=',
}


def generate_crap(num_items=100):
    """
    Return a list of dicts of {name: description}.

    :param num_items:
        Number of items to generate
    """
    names = set()
    while len(names) < num_items:
        names.add(fake.word().title())
    data = []
    for name in names:
        description = ' '.join(fake.words()).capitalize()
        item = {'name': name, 'description': description}
        data.append(item)
    return data


def populate_sites(site_data):
    """Populate sites from fixture data."""
    api = client.Client('http://localhost:8990/api', email='jathan@localhost')
    results = []
    for d in site_data:
        try:
            result = api.sites.post(d)
        except Exception as err:
            print err, d['name']
        else:
            results.append(result)
    print 'Created', len(results), 'sites.'


def generate_words(num_items=100):
    stuff = set()
    while len(stuff) < num_items:
        things = (fake.word(), fake.first_name(), fake.last_name())
        stuff.add(random.choice(things).title())
    return stuff


def generate_ips(num_items=100, version=4):
    stuff = set()
    while len(stuff) < num_items:
        if version == 4:
            ip = fake.ipv4()
        else:
            ip = fake.ipv6()
        stuff.add(ip)
    return stuff


def generate_devices(num_items=100):
    """
    Return a list of dicts of {name: description}.

    :param num_items:
        Number of items to generate
    """
    names = set()
    while len(names) < num_items:
        #names.add(fake.word().title())
        names.add(fake.word())
    data = []

    hostnames = generate_stuff(num_items)
    names = generate_stuff(num_items)
    values = generate_stuff(num_items)

    for name in names:
        description = ' '.join(fake.words()).capitalize()
        item = {'hostname': name, 'attributes': description}
        import json
        data.append(json.dumps(hashlib.sha1(item).hexdigest()))
    return data


@pytest.fixture
def config():
    fd, filepath = tempfile.mkstemp()
    config = dotfile.Dotfile(filepath)
    config.write(CONFIG_DATA)
    return config
