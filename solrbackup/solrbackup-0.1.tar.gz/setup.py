#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='solrbackup',
    version='0.1',
    description='Python script for backing up a remote Solr 4 core or SolrCloud cluster',
    author='National Library of Australia',
    author_email='ato@meshy.org',
    url='https://github.com/nla/solrbackup',
    license='MIT',
    packages=['solrbackup'])

