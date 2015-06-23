#!/usr/bin/env python

import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


version = ''
with open('bd/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')


dsc = ""
with open('README.rst', 'r') as f:
    dsc = f.read()


setup(
    name='BD',
    version=version,
    description='Bangladesh Details with postal code',
    long_description = dsc,
    author='Ahsan Habib',
    author_email='ahsan@vimmaniac.com',
    license = "MIT",
    url='https://vimmaniac.com/',
    packages=['bd'],
    package_data={'': ['LICENSE.txt']},
    include_package_data=True,
    keywords = ['BD', 'Bangladesh', 'Postal-Code', 'zip-code', 
                'District', 'Division', 'Thana'],
)
