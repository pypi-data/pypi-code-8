#!/usr/bin/env python
# coding=utf-8

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from ycyc import __version__
except ImportError:
    __version__ = "unknown version"


from setuptools import find_packages

dirname = os.path.dirname(__file__)

standard_exclude = ["*.py", "*.pyc", "*$py.class", "*~", ".*", "*.bak"]


def requirements_file_to_list():
    fn = os.path.join(dirname, "requirements.txt")
    with open(fn, 'rb') as f:
        return [x.rstrip() for x in list(f) if x and not x.startswith('#')]


setup(
    name='ycyc',
    version=__version__,
    description='a library by LYC',
    long_description=open('pypi.rst', 'a+').read(),
    author='Liu Yicong',
    author_email='imyikong@gmail.com',
    packages=find_packages(exclude=["tests.*", "tests"]),
    package_data={'': ['requirements.txt']},
    include_package_data=True,
    install_requires=requirements_file_to_list(),
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
