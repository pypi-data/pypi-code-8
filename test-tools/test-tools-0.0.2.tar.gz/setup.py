#!/usr/bin/env python
#
# Copyright 2015 Yuriy Gavenchuk aka murminathor
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

import os
import re

from setuptools import setup, find_packages


__author__ = 'y.gavenchuk aka murminathor'


version = re.compile(r'__version__\s*=\s*[\'"](.*?)[\'"]')


def get_package_version():
    """returns package version without importing it"""
    base = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(base, "test_tools/__init__.py")) as f:
        for line in f:
            m = version.match(line.strip())
            if not m:
                continue
            return m.group(1)


setup(
    name='test-tools',
    version=get_package_version(),
    description='Tools for unit testing: data_provider and FixtureManager',
    #long_description=open('README').read(),
    author='y.gavenchuk aka murminathor',
    author_email='murminathor@gmail.com',
    url='https://github.com/ygavenchuk/test-tools',
    license='Apache2',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent'
    ],
    packages=find_packages(exclude=['tests', 'tests.*']),
    dependency_links=[],
    install_requires=[],
    zip_safe=True
)
