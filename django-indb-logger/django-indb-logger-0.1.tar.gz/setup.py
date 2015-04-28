#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='django-indb-logger',
    version='0.1',
    description='Django app with in-database log handler',
    author='a1fred',
    author_email='demalf@gmail.com',
    license='MIT',
    url='https://github.com/a1fred/django-indb-logger',
    packages=['indb_logger'],
    platforms=['any'],
    zip_safe=False,
    install_requires=[
        'django>=1.4',
    ],
)
