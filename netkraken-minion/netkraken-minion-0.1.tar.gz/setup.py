#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'netkraken-minion',
          version = '0.1',
          description = '''records network connections: source host, protocol, target host''',
          long_description = '''records network connections: source host, protocol, target host''',
          author = "Arne Hilmann",
          author_email = "arne.hilmann@gmail.com",
          license = '',
          url = 'https://github.com/netkraken/minion',
          scripts = ['scripts/tags', 'scripts/record-connections'],
          packages = ['netkraken'],
          py_modules = [],
          classifiers = ['Development Status :: 3 - Alpha', 'Programming Language :: Python'],
          entry_points={
          'console_scripts':
              []
          },
             #  data files
             # package data
          install_requires = [ "countdb", "docopt" ],
          
          zip_safe=True
    )
