#!/usr/bin/env python
# -*- coding: UTF-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pybongtvapi import version

setup(
    name='pybongtvapi',
    version=version,
    description='a pythonic API for the bong.tv platform',
    long_description=open('README.rst').read(),
    author='Christian Maugg',
    author_email='software@christianmaugg.de',
    url='https://github.com/cmaugg/pybongtvapi',
    py_modules=['pybongtvapi', ],
    download_url='https://github.com/cmaugg/pybongtvapi/tarball/{0}'.format(version),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
    ],
    keywords='bong.tv pvr online video recorder epg electronic program guide',
)
