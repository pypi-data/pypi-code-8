#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import mezzanine_buffer

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = mezzanine_buffer.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='mezzanine-buffer',
    version=version,
    description="""Buffer integration for Mezzanine CMS""",
    long_description=readme + '\n\n' + history,
    author='Alex Tsai',
    author_email='caffodian@gmail.com',
    url='https://github.com/caffodian/mezzanine-buffer',
    packages=[
        'mezzanine_buffer',
    ],
    include_package_data=True,
    install_requires=[
        "requests >= 2.1.0",
        "buffer-python >= 1.08"
    ],
    dependency_links=[
        "https://github.com/vtemian/buffpy/tarball/master#egg=buffer-python-1.08"
    ],
    license="BSD",
    zip_safe=False,
    keywords='mezzanine-buffer',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)