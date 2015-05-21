#!/usr/bin/env python
"""
ezlogger
=====
ezlogger - The purpose of this module is to provide python scripters a very easy logging wrapper to handle more difficult to setup functions.
"""
from setuptools import setup

__version__ = '1.0.0'

dependencies = [
    "rainbow_logging_handler",
    "colorama",
]

setup(
    name='ezlogger',
    version=__version__,
    author='Gary Wright',
    author_email='zerosignal0@msn.com',
    url='https://github.com/zerosignal0/ezlogger/blob/master/README.md',
    description='ezlogger - The purpose of this module is to provide python scripters a very easy logging wrapper to handle more difficult to setup functions.',
    packages=['ezlogger'],
    zip_safe=False,
    install_requires=dependencies,
    license='Apache2',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
    ],
)
