#!/usr/bin/env python
import re

PROJECT = 'nekbot'
VERSION = open('VERSION').read().replace('\n', '')
MODULES = [
    'nekbot',
]
ROOT_INCLUDE = ['requirements.txt', 'VERSION', 'LICENSE.txt']
__author__ = 'nekmo'


from setuptools import setup, find_packages
from pip.req import parse_requirements

from distutils.util import convert_path
from fnmatch import fnmatchcase

import os
import sys
import glob
import uuid

try:
    long_description = open('README', 'rt').read()
except IOError:
    long_description = ''

__dir__ = os.path.abspath(os.path.dirname(__file__))

requirements = parse_requirements('requirements.txt', session=uuid.uuid1())
install_requires = [str(ir.req) for ir in requirements if not ir.url]

packages = find_packages(__dir__)
# Prevent include symbolic links
for package in tuple(packages):
    path = os.path.join(__dir__, package.replace('.', '/'))
    if not os.path.exists(path): continue
    if not os.path.islink(path): continue
    packages.remove(package)

# dependency_links = []
# for i, dependency in enumerate(install_requires):
#     if not re.findall('(hg|git|svn|bzr)\+', dependency): continue
#     install_requires[i] = dependency.split('#egg=')[1]
#     dependency_links.append(dependency.replace('-e ', ''))


##############################################################################
# find_package_data is an Ian Bicking creation.

# Provided as an attribute, so you can append to these instead
# of replicating them:
standard_exclude = ('*.py', '*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build',
                                './dist', 'EGG-INFO', '*.egg-info')


def find_package_data(where='.', package='',
                      exclude=standard_exclude,
                      exclude_directories=standard_exclude_directories,
                      only_in_packages=True,
                      show_ignored=False):
    """
    Return a dictionary suitable for use in ``package_data``
    in a distutils ``setup.py`` file.

    The dictionary looks like::

        {'package': [files]}

    Where ``files`` is a list of all the files in that package that
    don't match anything in ``exclude``.

    If ``only_in_packages`` is true, then top-level directories that
    are not packages won't be included (but directories under packages
    will).

    Directories matching any pattern in ``exclude_directories`` will
    be ignored; by default directories with leading ``.``, ``CVS``,
    and ``_darcs`` will be ignored.

    If ``show_ignored`` is true, then all the files that aren't
    included in package data are shown on stderr (for debugging
    purposes).

    Note patterns use wildcards, or can be exact paths (including
    leading ``./``), and all searching is case-insensitive.

    This function is by Ian Bicking.
    """

    out = {}
    stack = [(convert_path(where), '', package, only_in_packages)]
    while stack:
        where, prefix, package, only_in_packages = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                            or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            print >> sys.stderr, (
                                "Directory %s ignored by pattern %s"
                                % (fn, pattern))
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                    stack.append((fn, '', new_package, False))
                else:
                    stack.append(
                        (fn, prefix + name + '/', package, only_in_packages)
                    )
            elif package or not only_in_packages:
                # is a file
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                            or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            print >> sys.stderr, (
                                "File %s ignored by pattern %s"
                                % (fn, pattern))
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out
##############################################################################

description = 'NekBot, a modular multiprotocol bot.'
package_data = {'': ROOT_INCLUDE}

for module in MODULES:
    package_data.update(find_package_data(
        module,
        package=module,
        only_in_packages=False,
    ))

print(package_data)

setup(
    name=PROJECT,
    version=VERSION,

    description=description,
    long_description=long_description,

    author='Nekmo',
    author_email='contacto@nekmo.com',

    url='https://bitbucket.org/Nekmo/nekbot-mirai',

    classifiers=[
        'Natural Language :: Spanish',
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Topic :: Communications :: Chat',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
        'Topic :: Communications :: Conferencing',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    platforms=['linux'],

    provides=['nekbot'],
    install_requires=install_requires,

    packages=packages,
    include_package_data=True,
    # Scan the input for package information
    # to grab any data files (text, images, etc.)
    # associated with sub-packages.
    package_data=package_data,

    download_url='https://bitbucket.org/Nekmo/nekbot-mirai/get/default.tar.gz',
    keywords=['nekbot', 'bot', 'irc', 'xmpp', 'chat', 'telegram', 'jabber'],

    # entry_points={},

    zip_safe=False,
)