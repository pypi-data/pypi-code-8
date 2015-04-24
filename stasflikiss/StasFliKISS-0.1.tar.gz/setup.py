#! /usr/bin/env python
# -*- coding : utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

__author__ = u'Stas Evseev'
__version__ = u'0.1'
__appname__ = u'StasFliKISS'

from setuptools import setup, find_packages

requirements = []
for line in open('REQUIREMENTS.txt', 'r'):
    requirements.append(line)

setup(
    name=__appname__,
    version=__version__,
    packages=find_packages(),
    author=__author__,
    author_email='stasevseev@gmail.com',
    description='Wiki engine based on Markdown flat files powered by Flask. Fork from StasEvseev.',
    long_description=open('README.rst').read(),
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
    ],
)
