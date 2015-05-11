#!/usr/bin/env python
#coding:utf-8

from setuptools import setup, find_packages

setup(
    name = 'mabs',
    version = '0.1.4',
    keywords = ('mabs', 'egg'),
    description = 'used to control server by group with password,系统集中管理',
    license = 'mabsvs License',

    url = 'https://github.com/targetoyes/mabs',
    author = 'targetoyes',
    author_email = 'targetoyes@163.com',

    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = ["paramiko>=1.15.2", "sh>=1.11", "argparse>=1.2.1"],

    scripts=['bin/mabs'],

    package_data={'/etc/ansible/': ['mabs/hosts.ini', 'mabs/secret.ini']},
)
