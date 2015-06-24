# -*- coding: utf-8 -*-

#
# Copyright 2015 Jun-ya HASEBA
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
#

import os
from setuptools import find_packages, setup

from pyny import __version__


def read_file(file_name):
    base_path = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_path, file_name)
    if os.path.exists(file_path):
        return open(file_path).read()
    else:
        return ''


setup(
    name='pyny',
    version=__version__,
    description='Python wrapper around the Nagareyama Open Data Web API',
    long_description=read_file('README.rst'),
    author='Jun-ya HASEBA',
    author_email='7pairs@gmail.com',
    url='https://github.com/7pairs/pyny',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet',
    ],
    packages=find_packages(exclude=['tests']),
    keywords=['web', 'api', 'opendata', 'nagareyama'],
    license='Apache License, Version 2.0',
)
