#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
import os
import sys

py_version = sys.version_info
version = ".".join(
    [str(i) for i in __import__('pykongregate').__VERSION__]
)
readme = os.path.join(os.path.dirname(__file__), 'README.rst')

CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Natural Language :: English',
]

install_requires = [
    'simplejson',
    'requests'
]

setup(
    name='pykongregate',
    author='Korvyashka <korvyashka666@gmail.com>',
    version=version,

    author_email='korvyashka666@gmail.com',

    download_url='https://github.com/korvyashka/pykongregate.git',
    description='python client for kongreate REST API',
    long_description=open(readme).read(),
    license='MIT license',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=install_requires,
    packages=find_packages(exclude=['tests', 'docs']),
    test_suite='tests',
    include_package_data=True,
    zip_safe=False
)
