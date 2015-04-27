#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='pylfu',
    version='0.1.4',
    author='fengyun',
    author_email='rfyiamcool@163.com',
    packages=find_packages(),
    url='https://github.com/rfyiamcool',
    description='python Lfu cache service ',
    install_requires=['IPy==0.81'],
    license='MIT'
)
