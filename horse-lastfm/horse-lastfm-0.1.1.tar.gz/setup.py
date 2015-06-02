"""A setuptools based setup module for horse-lastfm.

https://github.com/grieve/horse-lastfm
"""

from os import path
from setuptools import setup
from setuptools import find_packages

here = path.abspath(path.dirname(__file__))

setup(
    name='horse-lastfm',
    version='0.1.1',

    description='LastFM integration bridle for Horse',
    long_description="""
""",

    url='https://github.com/grieve/horse-lastfm',

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

    keywords='chatbot slack chat bot communication lastfm',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[
        'horse',
        'pylast'
    ],

    extras_require={
        'dev': [],
        'test': [],
    },

    package_data={},
    data_files=[],
    entry_points={},
)
