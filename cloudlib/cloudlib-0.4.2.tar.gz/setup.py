#!/usr/bin/env python
# Copyright 2015, Kevin Carter.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools
import sys

import cloudlib


PACKAGES = [
    'cloudlib'
]


with open('requirements.txt') as f:
    required = f.read().splitlines()


if sys.version_info < (2, 6, 0):
    sys.stderr.write('This App Presently requires Python 2.6.0 or greater\n')
    raise SystemExit(
        '\nUpgrade python because you version of it is VERY deprecated\n'
    )
elif sys.version_info < (2, 7, 0):
    if 'argparse' not in required:
        required.append('argparse')


with open('README', 'rb') as r_file:
    LDINFO = r_file.read()
    LDINFO = LDINFO.decode('utf-8')


setuptools.setup(
    name=cloudlib.__appname__,
    version=cloudlib.__version__,
    author=cloudlib.__author__,
    author_email=cloudlib.__email__,
    description=cloudlib.__description__,
    long_description=LDINFO,
    license='Apache License Version 2.0',
    packages=PACKAGES,
    url=cloudlib.__url__,
    install_requires=required,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
