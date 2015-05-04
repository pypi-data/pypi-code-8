#!/usr/bin/env python
from setuptools import setup, find_packages


setup(name='kershaw',
      version='0.2.0',
      description='Kershaw General Purpose Utility Library',
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: IBM Public License',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3.4'],
      url='https://github.com/SPoage/kershaw',
      author='Shane Poage',
      author_email='SPoage@users.noreply.github.com',
      packages=find_packages())