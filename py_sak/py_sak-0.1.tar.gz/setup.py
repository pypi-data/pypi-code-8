'''
Package description and configuration.
To release to PyPI test:
  - python setup.py register -r pypitest
  - python setup.py sdist upload -r pypitest
To release to PyPI:
  - python setup.py register -r pypi
  - python setup.py sdist upload -r pypi
'''

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'py_sak',
    'packages': ['py_sak'],
    'install_requires': ['nose'],
    'version': '0.1',
    'description': 'Python Swiss Army Knife: common utilities and helpers for boilerplate code',
    'author': 'Marc CARRE',
    'author_email': 'carre.marc@gmail.com',
    'url': 'https://github.com/marccarre/py_sak',
    'download_url': 'https://github.com/marccarre/py_sak/tarball/0.1',
    'keywords': ['common', 'utilities', 'utility', 'utils', 'util', 'helpers', 'helper', 'input validation', 'validation'],
}

setup(**config)
