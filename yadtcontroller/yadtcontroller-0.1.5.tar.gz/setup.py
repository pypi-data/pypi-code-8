#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'yadtcontroller',
          version = '0.1.5',
          description = '''''',
          long_description = '''''',
          author = "Marcel Wolf, Maximilien Riehl, Michael Gruber",
          author_email = "marcel.wolf@immobilienscout24.de, maximilien.riehl@gmail.com, aelgru@gmail.com",
          license = 'GNU GPL v3',
          url = 'https://github.com/yadt/yadtcontroller',
          scripts = ['scripts/yadtcontroller'],
          packages = ['yadt_controller'],
          py_modules = [],
          classifiers = ['Development Status :: 3 - Alpha', 'Programming Language :: Python'],
          entry_points={
          'console_scripts':
              []
          },
             #  data files
             # package data
          install_requires = [ "Twisted", "docopt", "fysom", "requests", "yadtbroadcast-client-wamp2", "yadtcommons" ],
          
          zip_safe=True
    )
