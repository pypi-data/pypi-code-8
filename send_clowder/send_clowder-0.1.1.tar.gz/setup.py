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
    'clowder'
]

test_requirements = [
    'nose',
    'mock'
]

setup(
    name='send_clowder',
    version='0.1.1',
    description="Simple command-line tool for sending messages to clowder",
    long_description=readme + '\n\n' + history,
    author="Eric Scrivner",
    author_email='eric.t.scrivner@gmail.com',
    url='https://github.com/etscrivner/send_clowder',
    packages=[
        'send_clowder',
    ],
    package_dir={'send_clowder':
                 'send_clowder'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='send_clowder',
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
    tests_require=test_requirements,
    entry_points={
        'console_scripts': {
            'send_clowder = send_clowder.send_clowder:send_clowder_main'
        }
    }
)
