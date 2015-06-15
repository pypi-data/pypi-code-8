#!/usr/bin/env python

from setuptools import setup

setup(name='msdiff',
      version='0.1.0',
      description='Command and library to diff Musescore .mcsx files',
      author='Crypto',
      author_email='cryptonomicon.314@gmail.com',
      url='https://bitbucket.org/cryptonomicon314/msdiff',
      install_requires = [
        'lxml',
        'numpy'
      ],
      entry_points={
        'console_scripts': [
            'msdiff = msdiff.command_line:main',
        ]},
      zip_safe=False,
      packages=['msdiff'],
      test_suite = 'nose.collector',
      tests_require=['nose'],
     )
