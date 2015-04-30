# -*- coding: UTF-8 -*-
import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-gerencianet',
    version='0.1.2',
    packages=['gerencianet'],
    include_package_data=True,
    license='BSD License',  # example license
    description='Uma aplicação django para comunicar com o gateway de pagamento Gerencianet',
    long_description=README,
    url='http://www.starlinetecnologia.com.br/',
    author='Sidney Machado',
    author_email='sidney.machado@starlinetecnologia.com.br',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
    ],
)
