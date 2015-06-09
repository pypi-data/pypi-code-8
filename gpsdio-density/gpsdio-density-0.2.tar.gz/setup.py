#!/usr/bin/env python


"""
Setup script for gpsdio-density
"""


import os
from setuptools import setup


with open('README.rst') as f:
    readme = f.read().strip()


with open('LICENSE.txt') as f:
    license = f.read().strip()


version = None
author = None
email = None
source = None
with open(os.path.join('gpsdio_density', '__init__.py')) as f:
    for line in f:
        if line.strip().startswith('__version__'):
            version = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__author__'):
            author = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__email__'):
            email = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__source__'):
            source = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif None not in (version, author, email, source):
            break


setup(
    author=author,
    author_email=email,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Communications',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Utilities',
    ],
    description="A plugin for gpsdio for computing AIS density rasters.",
    entry_points='''
        [gpsdio.gpsdio_plugins]
        density=gpsdio_density.core:compute_density
    ''',
    extras_require={
        'test': ['pytest', 'pytest-cov']
    },
    include_package_data=True,
    install_requires=[
        'rasterio>=0.18',
        'click>=3.0',
        'Numpy>=1.7',
        'affine>=1.2',
        'gpsdio>=0.0.4'
    ],
    keywords='AIS GIS remote sensing raster',
    license=license,
    long_description=readme,
    name='gpsdio-density',
    packages=['gpsdio_density'],
    url=source,
    version=version,
    zip_safe=True
)
