#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='mistune-hilite',
    version='0.1.0',
    description='Python-Markdown Code Hilite port for Mistune',
    long_description=long_description,
    author='André Luiz',
    author_email='contato@xdvl.info',
    url='https://github.com/dvl/mistune-hilite',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup',
        'Topic :: Utilities',
    ],
    keywords='sintax highlight hilite mistune',
    packages=find_packages(),
    install_requires=[
        'mistune',
        'Pygments',
    ],
)
