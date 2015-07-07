from __future__ import absolute_import, print_function

import io
import os
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import relpath
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()

setup(
    name="digs",
    version="0.1.1",
    url="https://github.com/d555/digs",
    license='BSD',
    author="Jonathan S. Prieto C.",
    author_email="prieto.jona@gmail.com",
    description="For those who need to extract text to some depth over a website. Scraping Tasks",
    long_description='%s\n%s' % (
        read('README.rst'), re.sub(':obj:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    keywords=['crawling', 'crawler', 'web', 'text',
              'extraction', 'scraper', 'scrapy', 'scraping', 'links', 'html2txt', 'atxt'],
    install_requires=[
        'colorama==0.3.3', 'docopt==0.6.2', 'PySide==1.2.2', 'kitchen==1.2.1', 'aTXT>=1.0.5.4', 'beautifulsoup4==4.4.0', 'requests==2.7.0'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Utilities'
    ],
    entry_points={
        'console_scripts': [
            'digs = digs.__main__:main',
        ]
    },
)

# pandoc --from=rst --to=rst --output=README.rst README.rst
# Pasos para subir a pypi
# git tag v...
# python setup.py register -r pypi
# python setup.py sdist upload -r pypi
