#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

readme = open('README.rst').read()
requirements = open("requirements.txt").read().splitlines(),

setup(
    name='imgtohttps',
    version='0.3',
    description='Simple image uploader',
    long_description=readme,
    author='Andriy Kushnir (Orhideous)',
    author_email='orhideous@gmail.com',
    url='https://github.com/Orhideous/imgtohttps',
    packages=['imgtohttps'],
    package_dir={'imgtohttps': 'imgtohttps'},
    include_package_data=True,
    install_requires=requirements,
    license="GPLv3",
    zip_safe=False,
    keywords=['Imgur'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: No Input/Output (Daemon)",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Utilities",
    ],
)