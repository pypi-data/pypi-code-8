# -*- coding: utf-8 -*-
'''
@author: saaj
'''


try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup


setup(
  name             = 'Xmlify',
  version          = '0.1.1',
  author           = 'saaj',
  author_email     = 'mail@saaj.me',
  packages         = ['xmlify'],
  test_suite       = 'xmlify.test',
  url              = 'https://bitbucket.org/saaj/xmlify',
  license          = 'LGPL-2.1+',
  description      = 'Simple and fast Python built-in type XML serialiser',
  long_description = open('README.txt', 'rb').read().decode('utf-8'),
  platforms        = ['Any'],
  keywords         = 'python xml',
  classifiers      = [
    'Topic :: Software Development :: Libraries',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',    
    'Intended Audience :: Developers'
  ]
)

