#!/usr/bin/env python

import sys
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (2,5):
    raise NotImplementedError("Sorry, you need at least Python 2.5 or Python 3.x to use Doccu.")

setup(name='doccu',
      version='0.0.1',
      description='Documentation Storage, Retrieval and Version Management',
      author='James Milne',
      author_email='jmilne@graphic-designer.com',
      url='https://github.com/shakna-israel/doccu',
      py_modules=['doccu-manage'],
      scripts=['doccu-manage.py'],
      license='MIT',
      platforms = 'any',
      classifiers=['Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Text Processing'
     ]
     )

