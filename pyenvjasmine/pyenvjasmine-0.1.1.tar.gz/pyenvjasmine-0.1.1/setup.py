import os
import setuptools
from distutils.core import setup

version = '0.1.1'

requires = [
    'nose',
    'coverage'
]

setup(
    name='pyenvjasmine',
    version=version,
    description="A Python wrapper for envjasmine",
    long_description=open('README.rst').read(),
    author='Sascha Welter',
    author_email='',
    url='https://bitbucket.org/codigo23/pyenvjasmine',
    download_url='http://pypi.python.org/pypi/pyenvjasmine#downloads',
    license='BSD licence, see LICENSE',
    install_requires=requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: JavaScript',
        'Topic :: Software Development',
        'Topic :: Software Development :: Testing',
        ]
)
