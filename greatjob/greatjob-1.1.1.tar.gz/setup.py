#!/usr/bin/env python
from setuptools import setup, find_packages, Extension

setup(name='greatjob',
      version='1.1.1',
      description='Congratulations',
      author='Celeen Rusk',
      author_email='celeenrusk@gmail.com',
      liscense="MIT",
      packages=find_packages(),
      package_data={
            '': ['imageleap', 'sparkle.png', 'thumbsup.png', 'proj/*']
      },
      entry_points={
      	'console_scripts': [
      		'greatjob=greatjob:main'
      	]
      }
     )