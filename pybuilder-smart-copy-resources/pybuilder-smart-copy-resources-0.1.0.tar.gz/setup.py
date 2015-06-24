#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'pybuilder-smart-copy-resources',
          version = '0.1.0',
          description = '''PyBuilder plugin for copying additional resources''',
          long_description = '''''',
          author = "Martin Gruber",
          author_email = "martin.gruber@email.cz",
          license = 'MIT',
          url = 'https://github.com/margru/pybuilder-smart-copy-resources',
          scripts = [],
          packages = ['pybuilder_smart_copy_resources'],
          py_modules = [],
          classifiers = ['Development Status :: 2 - Pre-Alpha', 'License :: OSI Approved :: MIT License', 'Programming Language :: Python :: 2.7'],
          entry_points={
          'console_scripts':
              []
          },
             #  data files
             # package data
          
          
          zip_safe=True
    )
