# -*- coding: utf-8 -*-
"""
This module contains the tool of sample
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.3'

long_description = (
    read('README.rst')
    )

setup(name='nexiles.tools.api',
      version=version,
      description="nexiles.tools.api -- python nexiles Windchill gateway http client api",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      keywords='',
      author='Stefan Elethofer',
      author_email='stefan.eletzhofer@nexiles.com',
      url='https://skynet.nexiles.com/docs/nexiles.tools.api/',
      license='BSD',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['nexiles', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'requests',
                        'argparse',
                        'slumber',
                        # -*- Extra requirements: -*-
                        ],
     entry_points={
          'console_scripts': [
              'nxtools = nexiles.tools.api.main:main',
              ]
          }
      )
