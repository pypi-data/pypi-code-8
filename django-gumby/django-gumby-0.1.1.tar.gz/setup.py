#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import gumby

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = gumby.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-gumby',
    version=version,
    description="""Django health checks""",
    long_description=readme + '\n\n' + history,
    author='Luis Morales',
    author_email='luis.morales@kyperion.com',
    url='https://github.com/Kyperion/django-gumby',
    packages=[
        'gumby',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-gumby',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
