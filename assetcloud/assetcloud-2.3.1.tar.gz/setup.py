#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import re
import os
import sys


root_package_dir = 'apps'
packages = find_packages(root_package_dir)
main_package = 'assetcloud'

name = 'assetcloud'
description = 'Lightweight Digital Asset Management'
url = 'http://github.com/brightinteractive/assetcloud/'
author = 'Bright Interactive'
author_email = 'francis@bright-interactive.co.uk'
license = 'BSD'
install_requires = [
    # Standard packages:
    'boto==2.17.0',
    'dingus==0.3.4',
    'Django==1.6.11',
    'django_compressor==1.3',
    'django-debug-toolbar==0.11.0',
    'django-kombu==0.9.4',
    'django-haystack==2.2.0',
    'django-storages==1.1.8',
    'django-taggit==0.12.1',
    'Fabric==1.8.0',
    'pysolr==3.1.0',
    # Used by pysolr when Solr is running on Tomcat, even though pysolr doesn't declare a dependency on it
    'lxml==3.4.1',
    # ditto - also used by pysolr
    'cssselect==0.9.1',
    'sorl-thumbnail==11.12',
    'South==1.0.1',
    'Whoosh==2.4.1',
    'wsgiref==0.1.2',
    'django-social-auth==0.7.18',
    'bitstring==3.1.2',
    'django-dbbackup==1.80.2',
    'Pillow==2.5.3',

    # Bright packages on PyPI:
    'django-debug-error-logging==1.0.0',
    'django-raise-exception-view==1.0.1',
    'django-url-utils==1.0.0',
    'bright-vc==1.1.0',
    'django-validate-on-save==1.0.0',
    'django-url-history==1.0.1',
    'bright-fabric==0.0.2',

    # Packages used by tests:
    'django-test-extras==1.1.1',
    'beautifulsoup4==4.3.2',
    'coverage==3.7',
    'selenium==2.37.2',
    'webdriverplus==0.1.5',
    'unittest-xml-reporting==1.7.0',
    'django-model-utils==1.5.0',
    'ProxyTypes==0.9',
    'pep8==0.6.1',
    'pyflakes==0.5.0',
    'PyVirtualDisplay==0.1.2',
    'mock==1.0.1',
]


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(root_package_dir, package, '__init__.py')).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)


script_args = sys.argv[1:]
display_tag_message = False

if script_args and script_args[-1] == 'publish':
    script_args[-1:] = ['register', '-r',  'bright',  'sdist', 'upload', '-r', 'bright']
    display_tag_message = True


def relative_to_root(path):
    return os.path.relpath(path, root_package_dir)


setup(
    name=name,
    version=get_version(main_package),
    url=url,
    license=license,
    description=description,
    author=author,
    author_email=author_email,
    packages=packages,
    package_dir={'': root_package_dir},
    install_requires=install_requires,
    script_args=script_args,
    include_package_data=True,
    scripts=[root_package_dir + '/assetcloud/scripts/jenkinscisolr.sh']
)

if display_tag_message:
    args = {'version': get_version(main_package)}
    print "You probably want to also tag the version now:"
    print "  git tag -a v%(version)s -m 'Version %(version)s'" % args
    print "  git push --tags"
