# -*- coding: utf-8 -*-
# Copyright (c) 2015 Tomek Wójcik <tomek@bthlabs.pl>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import codecs
from setuptools import setup
import sys

desc_file = codecs.open('README.rst', 'r', 'utf-8')
long_description = desc_file.read()
desc_file.close()

meta = {}
with open('osxnotify_cffi/meta.py', 'r') as f:
    exec(compile(f.read(), 'osxnotify_cffi/meta.py', 'exec'), meta)

setup(
    name=meta['__title__'].encode('utf-8'),
    version=meta['__version__'],
    description=(
        'No nonsense OS X notifications for Python scripts (CFFI wrapper)'
    ),
    long_description=long_description,
    author=meta['__author__'].encode('utf-8'),
    author_email='tomek@bthlabs.pl',
    packages=['osxnotify_cffi'],
    install_requires=['cffi>=1.0.0'],
    license=meta['__license__'].encode('utf-8'),
    url='https://github.com/tomekwojcik/osxnotify-python-cffi',
    download_url=(
        'http://github.com/tomekwojcik/osxnotify-python-cffi/tarball/v%s' %
        meta['__version__']
    ),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: MacOS X :: Cocoa",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
