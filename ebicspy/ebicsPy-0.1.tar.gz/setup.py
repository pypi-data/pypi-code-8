#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='ebicsPy',
      py_modules=['ebicsPy'],
      version='0.1',
      description='Client side library for the banking communication EBICS protocol',
      keywords = ["EBICS", "Banking communication"],
      
      author='Aurélien DUMAINE',
      author_email='aurelien@dumaine.me',
      license = 'GNU Affero General Public License',
      url = 'http://pypi.python.org/pypi/ebicsPy',

      classifiers = ['Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Security :: Cryptography'],
        long_description = '''\

This is an open source Python library dealing with the EBICS protocole on client side.

The newest version of this module can be found there :
https://code.launchpad.net/~aurelien-dumaine/+junk/ebicspy

Examples in the README.txt file
'''
      )
