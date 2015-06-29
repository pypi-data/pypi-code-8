"""This file defines how dump2json is installed in a python environment.
"""
import setuptools

setuptools.setup(
    name='pytest-dump2json',
    version='0.1.0',
    description = 'A pytest plugin for dumping test results to json.',
    py_modules=['dump2json'],
    install_requires=['pytest'],
    test_suite='test',
    entry_points = {
        'pytest11': [
            'pytest-dump2json = dump2json',
        ]
    },
    author = 'Danielle Jenkins',
    author_email = 'jenkinda@uw.edu',
    keywords = ['testing', 'pytest', 'json'],
    url = 'https://github.com/d6e/pytest-dump2json',
    download_url = 'https://github.com/d6e/pytest-dump2json/archive/0.1.0.zip',
)
