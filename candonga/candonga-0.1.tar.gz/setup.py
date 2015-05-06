#!/usr/bin/env python

PROJECT = 'candonga'

# Change docs/sphinx/conf.py too!
VERSION = '0.1'

from setuptools import setup, find_packages

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='Candonga Framework',
    long_description=long_description,

    author='Raul Robledo',
    author_email='raul.osvaldo.robledo@gmail.com',

    url='https://github.com/rrobledo/candonga',
    download_url='https://github.com/rrobledo/candonga.git',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'candonga = candonga.main:main'
        ],
        'candonga.commands': [
            'create-infra-project = candonga.command:CreateInfraProject',
            'create-project = candonga.command:CreateProject',
        ],
    },

    zip_safe=False,
)
