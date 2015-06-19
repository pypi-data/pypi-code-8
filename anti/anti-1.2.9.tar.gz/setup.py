#!/usr/bin/env python

from setuptools import setup

bitbucket_url = 'https://gprohorenko@bitbucket.org/gprohorenko/anti'

setup(
    name='anti',
    version='1.2.9',
    description='SeoUtils',
    long_description=open('README.rst', 'r').read(),
    author='blinchik',
    author_email='prohorenko_gena_@mail.ru',
    download_url='https://bitbucket.org/gprohorenko/anti/downloads/anti.tar.gz',
    url=bitbucket_url,
    include_package_data=True,
    license='MIT License',
    zip_safe=False,
    packages=['anti'],
    install_requires=[
        "beautifulsoup4",
        "requests",
        "Flask-Migrate",
        "Flask-SQLAlchemy",
        "psycopg2",
        "redis",
        "python-whois",
    ],
)
