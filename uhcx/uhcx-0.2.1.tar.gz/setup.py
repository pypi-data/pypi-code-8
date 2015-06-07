"""
Python library for the uh.cx link shortener.

http://uh.cx/
"""

from distutils.core import setup

from setuptools import find_packages


setup(
    name='uhcx',
    version='0.2.1',
    author='J. Boehm',
    author_email='jb@uh.cx',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    url='http://uh.cx/',
    license='MIT',
    description='Library for the uh.cx link shortener.',
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
