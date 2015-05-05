#!/usr/bin/env python

from setuptools import setup

setup(name='sps',
      version='0.6.0',
      description='A simple pubsub framework (soon to be) with included REST API',
      author='iLoveTux',
      author_email='me@ilovetux.com',
      maintainer="ilovetux",
      url='https://github.com/iLoveTux/simple_pubsub',
      packages=['sps'],
      license="GPL v2",
      install_requires=["bottle == 0.12.8"]
     )
