#!/usr/bin/env python
# -*- coding:utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import ocapi.info as pkg


if __name__ == "__main__":
    name = pkg.__name__.split(".")[0]
    setup(
      name=name,
      packages=[name],
      version=pkg.__version__,
      author=pkg.__author__,
      author_email=pkg.__email__,
      long_description=open("README.rst").read(),
      url=pkg.__web__,
      keywords=[name, 'automatization', 'api'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
      test_suite="test")
