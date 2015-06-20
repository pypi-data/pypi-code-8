#!/usr/bin/env python

from setuptools import setup

setup(
    name='sunset',
    version='0.1',
    packages=['sunset'],
    author='Jimmy Shen',
    author_email='thejimmyshen@gmail.com',
    description='Use comments to add expiration dates to your code.',
    license='MIT',
    entry_points={'console_scripts': ['sunset = sunset.bin:main']},
    install_requires=[],
    url='https://github.com/jimmyshen/sunset',
    download_url='https://github.com/jimmyshen/sunset/tarball/0.1',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License'
    ]
)
