#
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages
import os.path
import sys
readme_path = os.path.join(os.path.dirname(__file__), 'README.rst')
if sys.hexversion < 0x03000000:
    doc = open(readme_path).read()
else:
    doc = open(readme_path, encoding='utf-8').read()

setup(
  name = 'unicode_ids',
  version = '2.0.5',
  author = u'Suzumizaki-Kimitaka(\u9234\u898b\u54b2 \u541b\u9ad8)',
  author_email = 'info@h12u.com',
  url = 'http://h12u.com/sphinx/unicode_ids/',
  license = 'BSD',
  description = 'Enable Sphinx to generate non-ASCII identifiers',
  packages = find_packages(),
  package_data = {
    '' : [ 'sphinxcontrib/*', 'sphinxcontrib/unicode_ids/*',
           'doc/*.bat', 'doc/Makefile', 'doc/conf.py', 'doc/*.rst',
           'doc/_build/html/*.html', 'doc/_build/html/*.js',
           'doc/_build/html/_sources/*', 'doc/_build/html/_static/*',
         ],
  },
  entry_points = {},
  install_requires = ['sphinx>=1.3.1'],
  platforms = 'any',
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Environment :: Web Environment',
    'Framework :: Sphinx',
    'Framework :: Sphinx :: Extension',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Documentation',
    'Topic :: Documentation :: Sphinx',
    'Topic :: Text Processing',
    'Topic :: Utilities',
  ],
  long_description = doc,
)
