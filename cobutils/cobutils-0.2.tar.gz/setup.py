#!/usr/bin/python
#from distutils.core import setup
from setuptools import setup
import os
README = os.path.join(os.path.dirname(__file__), 'README.txt')

long_description = open(README).read() + '\n\n'

setup(name='cobutils',
      version='0.2',
      description='MAnipulate cobol files from python',
      author='Ferran Pegueroles Forcadell',
      author_email='ferran@pegueroles.com',
      url='http://www.pegueroles.com/',
      long_description=long_description,
      license='GPL',
      packages=['cobutils'],
      scripts=["cobextract.py", "cobcreate.py"],
      data_files=[])
