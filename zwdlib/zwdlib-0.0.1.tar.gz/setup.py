'''
Created on Jun 20, 2015

@author: root
'''
from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name = 'zwdlib',
    version = '0.0.1',
    keywords = ('common', 'tools'),
    description = 'most common used tools',
    license = 'MIT License',

    author = 'winston',
    author_email = 'a18190@qq.com',

    packages = find_packages(),
    platforms = 'any',
)