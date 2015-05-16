from __future__ import absolute_import
from setuptools import setup

setup(
    name='gavagai',
    packages=['gavagai'],
    version='0.2.7',
    description='A Gavagai API helper library.',
    author='Johan Dewe',
    author_email='johan@dewe.net',
    url='https://github.com/dewe/gavagai-python',
    keywords=['text-analysis', 'api', 'nlp'], 
    classifiers=['Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.3'],
    license='The MIT License (MIT)',
    install_requires=[
        'requests>=2.7.0,<3.0',
        'six==1.9.0',
        'ndg-httpsclient==0.4.0',
    ]
)