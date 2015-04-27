#!/usr/bin/env python

from setuptools import setup
from twypy import __author__, __version__

import os
import sys

setup(
    name = 'twypy',
    version = __version__,
    install_requires = ('requests_oauthlib>=0.3.2'),
    author = 'Roger Fernandez Guri',
    author_email = 'rogerfernandezguri@me.com',
    license = open('LICENSE').read(),
    url = 'https://github.com/rogerfernandezg/twypy/',
    keywords = 'twitter rest api',
    description = 'Twitter REST API v1.1 client for Python',
    long_description = open('README.md').read(),
    include_package_data = True,
    packages = (
        'twypy',
    ),
    classifiers = (
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    )
)
