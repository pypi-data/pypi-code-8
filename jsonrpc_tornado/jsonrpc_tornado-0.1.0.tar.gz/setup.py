#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os.path
import re

with open(os.path.join(os.path.dirname(__file__),
                       'jsonrpc_tornado', '__init__.py')) as v_file:
    VERSION = re.compile(r".*__version__\s*=\s*'(.*?)'", re.S).match(v_file.read()).group(1)

setup(
    name='jsonrpc_tornado',
    version=VERSION,
    description='Asynchronous JSON-RPC client for Tornado',
    keywords='json-rpc tornado asynchronous non-blocking',
    author='Artem Mustafa',
    author_email='artemmus@yahoo.com',
    url='https://github.com/artemmus/jsonrpc_tornado',
    long_description=open('README.rst').read(),
    packages=['jsonrpc_tornado',],
    requires=['tornado'],
    install_requires=['tornado'],
    tests_require=['mock'],
    include_package_data = True,    
    platforms = ('Any',),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Freeware',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)