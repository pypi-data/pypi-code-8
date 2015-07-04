# -*- coding: utf-8 -*-
'''
@author: saaj
'''


try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup
  
  
setup(
  name             = 'Fangorn',
  version          = '0.3.0',
  author           = 'saaj',
  author_email     = 'mail@saaj.me',
  packages         = ['fangorn', 'fangorn.compat', 'fangorn.test'],
  package_data     = {'fangorn.test' : ['fixture/*']},
  test_suite       = 'fangorn.test',
  url              = 'https://bitbucket.org/saaj/fangorn',
  license          = 'LGPL-2.1+',
  description      = 'Nested Sets SQL Tree for Python',
  long_description = open('README.txt', 'rb').read().decode('utf-8'),
  platforms        = ['Any'],
  keywords         = 'python tree nested-sets mysql sqlite',
  classifiers      = [
    'Topic :: Database',
    'Topic :: Software Development :: Libraries',    
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',  
    'Intended Audience :: Developers'
  ]
)