# coding: utf-8

from setuptools import setup, find_packages
import os.path
doc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
  name = 'sphinx_html5_basic_theme',
  version = '1.0.4',
  author = 'Suzumizaki-Kimitaka(鈴見咲 君高)',
  author_email = 'info@h12u.com',
  url = 'http://h12u.com/sphinx/html5_basic_theme/',
  license = 'BSD',
  description = 'Enable Sphinx to generate HTML5 valid files',
  packages = find_packages(),
  package_data = {
    '' : ['html5_*/*.html', 'html5_*/*.xml', 'html5_*/*.conf',
          'html5_*/static/*', 'html5_*/changes/*',
          'doc/*.bat', 'doc/Makefile', 'doc/conf.py', 'doc/*.rst' ],
  },
  entry_points = {
    'sphinx_themes': ['path = sphinx_html5_basic_theme.setup_get_path:get_path', ],
  },
  install_requires = ['sphinx>=1.3'],
  platforms = 'any',
  classifiers = [
    "Framework :: Sphinx :: Extension",
    "Framework :: Sphinx :: Theme",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Topic :: Documentation :: Sphinx",
    "Topic :: Software Development :: Documentation",
  ],
  long_description = doc,
)
