#!/usr/bin/env python

import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

version = ''
with open('arisutils/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')


setup(
    name='arisutils',
    packages=['arisutils'],
    version=version,
    zip_safe=False,

    author='Aris Pikeas',
    author_email='aris@pike.as',
    description='TODO',
    license='TODO',
    url='TODO',
)
