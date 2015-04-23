#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='harvest_api_client',
    version='1.1.3',
    description='A client for the Harvest API (getharvest.com)',
    license='MIT',
    author='Alex Maslakov',
    author_email='Alex Maslakov<me@gildedhonour.com>, Alex Maslakov<gilded.honour@gmail.com>',
    url='https://github.com/GildedHonour/harvest-api-client',
    packages=['harvest_api_client'],
    long_description=long_description,
    keywords = ['harvest-api', 'api', 'harvest.com', 'getharvest.com', 'harvest', 'api client'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
    ],  
)