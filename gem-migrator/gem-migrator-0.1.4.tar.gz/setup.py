from __future__ import unicode_literals
from setuptools import setup, find_packages

setup(name='gem-migrator',
      version = '0.1.4',
      description = 'utility for migrating Gem application wallets',
      url = 'http://github.com/GemHQ/gem-migrator',
      author = 'Matt Smith',
      author_email = 'matt@gem.co',
      license = 'MIT',
      packages = find_packages(),
      install_requires = [
          'PyNaCl==0.3.0',
          'round==0.9.0'
      ],
      tests_require = [ 'tox' ],
      scripts=[ 'gem-migrator' ],
      zip_safe=False)
