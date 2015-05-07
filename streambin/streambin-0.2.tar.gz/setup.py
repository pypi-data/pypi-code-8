#!/usr/bin/env python
#
#   Copyright 2015 Linux2Go
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from setuptools import setup, find_packages

setup(
    name='streambin',
    description='Client for Streambin.net',
    author='Soren Hansen',
    author_email='soren@linux2go.dk',
    url='http://streambin.net/',
    version='0.2',
    packages=['streambin'],
    zip_safe=True,
    install_requires=['requests'],
    entry_points={'console_scripts': ['streambin=streambin:main']}
)

