#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(

    name='kite-mail',
    description='kite-mail is a command-line tool to request the contents of e-mail to takosan .',
    version='0.0.0.dev0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'kite-string',
        'pyzmail',
        ],
    entry_points='''
        [console_scripts]
        kite-mail=kite_mail.cli:main
    ''',
    author = 'Kei Iwasaki',
    author_email = 'me@laughk.org',
    license = 'MIT License',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

)
