#!/usr/bin/env python
#coding:utf8

from setuptools import setup,find_packages

setup(
   name='essun-test',
   version='0.0.1',
   url="http://www.google.com",
   license='MIT',
   author='Kinggp',
   author_email='jinlinger.love@163.com',
   description="a description test framework",
   platforms='any',
   keywords='framework nose testing',
   packages=find_packages(exclude=['test1']),
   install_requires= ["tox"]



)
