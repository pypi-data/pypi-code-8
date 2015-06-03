"""A setuptools based setup module for horse-google.

https://github.com/grieve/horse-google
"""

from os import path
from setuptools import setup
from setuptools import find_packages

here = path.abspath(path.dirname(__file__))

setup(
    name='horse-google',
    version='0.1.3',

    description='Google API integration bridles for Horse',
    long_description="""
""",

    url='https://github.com/grieve/horse-google',

    author='Ryan Grieve',
    author_email='me@ryangrieve.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Chat',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='chatbot slack chat bot communication google',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[
        'horse',
        'oauth2client',
        'google-api-python-client'
    ],

    extras_require={
        'dev': [],
        'test': [],
    },

    package_data={},
    data_files=[],
    entry_points={},
)
