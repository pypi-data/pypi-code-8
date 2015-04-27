#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

VERSION = '1.3'

setup(
    name='django-secureadmin',
    version=VERSION,
    description="Django-SecureAdmin send verification mail when user last and new ip not equals.",
    long_description=(
        open("README.rst").read()),
    keywords='secure django,django,secure django admin,django admin,secureadmin',
    author='Mahdi Fakhrabadi',
    author_email='mahdi.blackhat@gmail.com',
    url='https://github.com/irandjango/django-secureadmin/',
    license='MIT',
    package_dir={'secureadmin': 'secureadmin'},
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Security',
    ],
    zip_safe=False,
)
