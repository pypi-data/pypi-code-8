#!/usr/bin/env python

from os.path import exists
from setuptools import setup, find_packages

from django_image import __version__

setup(
    name='django-image',
    version=__version__,
    # Your name & email here
    author='Adam Charnock',
    author_email='adam@adamcharnock.com',
    # If you had django_image.tests, you would also include that in this list
    packages=find_packages(),
    # Any executable scripts, typically in 'bin'. E.g 'bin/do-something.py'
    scripts=[],
    # REQUIRED: Your project's URL
    url='http://github.com/adamcharnock/django-image',
    # Put your license here. See LICENSE.txt for more information
    license='MIT',
    # Put a nice one-liner description here
    description='Simple pluggable framework for displaying images in Django',
    long_description=open('README.rst').read() if exists("README.rst") else "",
    # Any requirements here, e.g. "Django >= 1.1.1"
    install_requires=[
        'django>=1.7',
    ],
)
