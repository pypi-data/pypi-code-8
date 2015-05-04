# coding: utf-8

#import numpy as np
from distutils.core import setup

from Cython.Distutils import Extension, build_ext
from Cython.Compiler import Options
from Cython.Build import cythonize

Options.fast_fail = True
Options.binding = False
    
ext_modules = [
    Extension(
        "arraybuffer.arraybuffer",
        ["lib/arraybuffer/arraybuffer.pyx"],
    ),
]

long_description = open('README.rst').read()

setup(
    name = 'arraybuffer',
    version = '0.1.1',
    description = 'Cython based buffer for arrays and typed memoryviews.',
    author = 'Zaur Shibzukhov',
    author_email="szport@gmail.com",
    license="MIT License",
    ext_modules = cythonize(ext_modules),
    package_dir = {'': 'lib'},
    packages = ['arraybuffer', ],
    package_data={'': ['*.pxd']},
    url = 'https://bitbucket.org/intellimath/arraybuffer',
    download_url = 'https://bitbucket.org/intellimath/arraybuffer',
    long_description = long_description,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
