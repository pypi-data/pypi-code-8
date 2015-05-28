#!/usr/bin/env python

from setuptools import setup

setup(name = 'metameta',
      version = '0.0.0.20',
      description = 'Toolkit for analyzing '\
          + 'meta-transcriptome/metagenome mapping data',
      classifiers = [
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.4',
            'Topic :: Scientific/Engineering :: Bio-Informatics'
          ],
      keywords = 'bioinformatics metadata metagenome metatranscriptome'\
          + 'short reads mapping alignment',
      url = 'https://github.com/Brazelton-Lab/metameta/',
      download_url = 'https://github.com/Brazelton-Lab/metameta/tarball/'\
          + '0.0.0.20',
      author = 'Alex Hyer',
      author_email = 'theonehyer@gmail.com',
      license = 'GPL',
      packages = ['metameta'],
      include_package_data = True,
      zip_safe = False,
      install_requires = [
          'argparse',
          'pysam',
          'statistics',
          're'
          ],
      entry_points = {
        'console_scripts':['metameta = metameta.__main__:main']
        },
      )
