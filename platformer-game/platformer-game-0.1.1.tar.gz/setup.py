#!/usr/bin/env python

from setuptools import setup

setup(
    name='platformer-game',
    version='0.1.1',
    description="atmospheric platformer game",
    long_description=open('README.rst').read(),
    author='Tobias Bengfort',
    author_email='tobias.bengfort@gmx.net',
    packages=['platformer'],
    include_package_data=True,
    entry_points={'console_scripts': 'platformer=platformer:main'},
    install_requires=[
        'pygame',
    ],
    license='GPLv3+',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License v3 or later '
            '(GPLv3+)',
        'Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games',
    ])
