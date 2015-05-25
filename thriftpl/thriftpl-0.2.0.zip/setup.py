# coding: utf-8

from setuptools import setup, find_packages
from codecs import open
from os import path


with open(path.join( path.abspath(path.dirname(__file__)), 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="thriftpl",
    version="0.2.0",
	
	
	description="a thrift client pool for python",
	long_description=long_description,
	
	author="tanghd",
	author_email="hand515@gmail.com",
	
	url="http://git.oschina.net/hand515/python-thrift-pool",
	license="LGPL",
	
	packages = find_packages(exclude=["tests"]),
    install_requires=[
        "thrift",
    ],
)