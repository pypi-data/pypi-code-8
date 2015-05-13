from setuptools import setup, find_packages
from cmsplugin_catalog import __version__

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Communications',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards',
    'Topic :: Internet :: WWW/HTTP :: Site Management',
    'Programming Language :: Python :: 2.7',
]

config = {
    'name': 'cmsplugin-catalog',
    'description': 'Django CMS page catalog plugin',
    'long_description': open('README.rst').read(),
    'url': 'http://github.com/tkliuxing/cmsplugin-catalog',
    'author': 'Ronald White',
    'author_email': 'ouyanghongyu@gmail.com',
    'license': 'MIT',
    'version': __version__,
    'install_requires': ['django-cms<3.1',],
    'tests_require': ['tox>=1.8'],
    'packages': find_packages(),
    'include_package_data': True,
    'platforms': ['OS Independent'],
    'scripts': [],
    'zip_safe': False,
    'classifiers': CLASSIFIERS,
}

setup(**config)
