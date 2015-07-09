from setuptools import setup, find_packages

version = '0.0.11'
name = 'ortoolpy'
short_description = '`ortoolpy` is a package for ortoolpy.'
long_description = """\
`ortoolpy` is a package for ortoolpy.
::

   from ortoolpy import knapsack
   size = [21, 11, 15, 9, 34, 25, 41, 52]
   weight = [22, 12, 16, 10, 35, 26, 42, 53]
   capacity = 100
   knapsack(size, weight, capacity)

Requirements
------------
* Python 2 or Python 3, numpy, networkx, pulp

Features
--------
* This is a sample. So it may not be efficient.

Setup
-----
::

   $ pip install ortoolpy
   or
   $ easy_install ortoolpy

History
-------
0.0.1 (2015-6-26)
~~~~~~~~~~~~~~~~~~
* first release

"""

classifiers = [
   "Development Status :: 1 - Planning",
   "License :: OSI Approved :: Python Software Foundation License",
   "Programming Language :: Python",
   "Topic :: Software Development",
]

setup(
    name=name,
    version=version,
    description=short_description,
    long_description=long_description,
    classifiers=classifiers,
    #py_modules=['ortoolpy'],
    packages=find_packages(),
    keywords=['ortoolpy',],
    author='Saito Tsutomu',
    author_email='tsutomu@kke.co.jp',
    url='https://pypi.python.org/pypi/ortoolpy',
    license='PSFL',
    install_requires=['numpy', 'networkx', 'pulp', ],
)