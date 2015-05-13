# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


def readfile(fn):
    """Read fn and return the contents."""
    with open(path.join(here, fn), 'r', encoding='utf-8') as f:
        return f.read()

setup(
      name='narmer',
      packages=find_packages(exclude=['tests*']),
      version='0.1.1',
      description='Narmer Experimental NLP/IR library for Python',
      author='Christopher C. Little',
      author_email='chrisclittle+narmer@gmail.com',
      url='https://github.com/chrislit/narmer',
      download_url='https://github.com/chrislit/narmer/archive/master.zip',
      keywords=['nlp', 'ai', 'ir', 'language', 'linguistics',
                'phonetic algorithms'],
      license='GPLv3+',
      classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 or later \
(GPLv3+)',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic',
        ],
      long_description='\n\n'.join([readfile(f) for f in ('README.rst',
                                                          'HISTORY.rst',
                                                          'AUTHORS.rst')]),
      install_requires=['abydos'],
      )
