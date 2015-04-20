#!/usr/bin/env python

import os
from setuptools import setup
from spanner import __version__

d = os.path.realpath(os.path.dirname(__file__))
with open(os.path.join(d, 'requirements.txt'), 'r') as fh:
    reqs = [i.strip() for i in fh]

setup(
    name='spanner',
    version=__version__,
    description='An accumulation of utilities / convenience functions for python',
    author='Bryan Johnson',
    author_email='d.bryan.johnson@gmail.com',
    packages=['spanner'],
    url='https://github.com/dbjohnson/python-utils',
    download_url='https://github.com/dbjohnson/spanner/tarball/%s' % __version__,
    install_requires=reqs
)
