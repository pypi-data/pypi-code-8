#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'countdb',
          version = '0.2',
          description = '''''',
          long_description = '''count events, store in plain files, aggregate over time''',
          author = "Arne Hilmann",
          author_email = "arne.hilmann@gmail.com",
          license = '',
          url = 'https://github.com/netkraken/countdb',
          scripts = [],
          packages = ['countdb'],
          py_modules = [],
          classifiers = ['Development Status :: 3 - Alpha', 'Programming Language :: Python'],
          entry_points={
          'console_scripts':
              []
          },
             #  data files
             # package data
          install_requires = [ "docopt" ],
          
          zip_safe=True
    )
