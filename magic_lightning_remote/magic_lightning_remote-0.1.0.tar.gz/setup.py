#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'flask'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='magic_lightning_remote',
    version='0.1.0',
    description="Web controller for the magic lightning irda lamplight (acheap rgb irda controlled lightbulb)",
    long_description=readme + '\n\n' + history,
    author="David Francos Cuartero",
    author_email='me@davidfrancos.net',
    url='https://github.com/XayOn/magic_lightning_remote',
    packages=[
        'magic_lightning_remote',
    ],
    package_dir={'magic_lightning_remote':
                 'magic_lightning_remote'},
    include_package_data=True,
    package_data = {
        'magic_lightning_remote': ['*.json', 'templates/*.html']
    },
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='magic_lightning_remote',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
