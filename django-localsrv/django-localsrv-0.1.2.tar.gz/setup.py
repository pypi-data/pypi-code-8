#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

import io
import os
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import relpath
from os.path import splitext

from setuptools import find_packages
from setuptools import setup
from setuptools.command import develop


class Develop(develop.develop):
    def run(self, *args, **kwargs):
        import pydevd; pydevd.settrace()
        develop.run(*args, **kwargs)


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='django-localsrv',
    version='0.1.2',
    license='MIT',
    description="Django app for serving static content from different sources (files, strings, urls, etc.) at custom paths, using custom HTTP headers. Intended as a more flexible option than Python's SimpleHTTPServer",
    long_description='%s\n%s' % (read('README.rst'), re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))),
    author='Vlad George Ardelean',
    author_email='asdf@yopmail.com',
    url='https://github.com/vladiibine/localsrv',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=False,
    zip_safe=False,

    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
    ],
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    install_requires=[
        'django>=1.8,<1.9', 'requests>=2.6,<2.7'
    ],
    extras_require={
        # eg: 'rst': ['docutils>=0.11'],
    },
    entry_points={
        'console_scripts': [
            'localsrv = localsrv.__main__:main',
        ]
    },
)
