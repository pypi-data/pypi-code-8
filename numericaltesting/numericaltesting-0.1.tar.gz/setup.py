#!/usr/bin/env python
from distutils.core import setup

setup(name='numericaltesting',
      description='Tools for unittesting with arrays and numerical algorithms',
      version='0.1',
      author='Alex Flint',
      author_email='alex.flint@gmail.com',
      url='https://github.com/alexflint/numericaltesting',
      packages=['numericaltesting'],
      package_dir={'numericaltesting': '.'},
      )
