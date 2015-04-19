#!/usr/bin/env python

from setuptools import setup

setup(name='check-graylog-lag',
      version='1.0',
      description='Nagios plugin to check graylog lag',
      author='Ilya Margolin',
      author_email='ilya@jimdo.com',
      scripts=['check_graylog_lag'],
      install_requires=open('requirements.txt').readlines(),
      )
