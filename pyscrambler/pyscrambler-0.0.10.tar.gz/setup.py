#!/usr/bin/python

from setuptools import setup


setup(
    name='pyscrambler',
    version='0.0.10',
    description='Concept data scrambler using permutations as a basis',
    url='https://github.com/saxbophone/pyscrambler',
    author='Joshua Saxby',
    author_email='joshua.a.saxby@gmail.com',
    license='MIT',
    packages=['pyscrambler', 'pyscrambler.scramblers'],
    install_requires=['bitstring==3.1.3',
                      'oset==0.1.3'],
    extras_require={
        'test': ['coverage==3.7.1'],
    },
    zip_safe=False
)
