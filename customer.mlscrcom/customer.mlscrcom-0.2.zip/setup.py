# -*- coding: utf-8 -*-

###############################################################################
#
# Copyright (c) 2011 Propertyshelf, Inc. and its Contributors.
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
###############################################################################
"""Setup for the customer.mlscrcom package."""

import os
import sys
from setuptools import setup, find_packages

sys.path.insert(0, os.path.abspath('src/'))


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


def check_server(server):
    if not server:
        return

    COMMANDS_WATCHED = ('register', 'upload')

    changed = False

    for command in COMMANDS_WATCHED:
        if command in sys.argv:
            # Found one command, check for -r or --repository.
            commandpos = sys.argv.index(command)
            i = commandpos + 1
            repo = None
            while i < len(sys.argv) and sys.argv[i].startswith('-'):
                # Check all following options (not commands).
                if (sys.argv[i] == '-r') or (sys.argv[i] == '--repository'):
                    # Next one is the repository itself.
                    try:
                        repo = sys.argv[i + 1]
                        if repo.lower() != server.lower():
                            print "You tried to %s to %s, while this package "\
                                  "is locked to %s" % (command, repo, server)
                            sys.exit(1)
                        else:
                            # Repo is OK.
                            pass
                    except IndexError:
                        # End of args.
                        pass
                i = i + 1

            if repo is None:
                # No repo found for the command.
                print "Adding repository %s to the command %s" % (
                    server, command)
                sys.argv[commandpos + 1: commandpos + 1] = ['-r', server]
                changed = True

    if changed:
        print "Final command: %s" % (' '.join(sys.argv))


setup(
    name='customer.mlscrcom',
    version=0.2,
    description="mls-cr.com Theme & Policy Product.",
    long_description='\n\n'.join([
        open(os.path.join('README.txt')).read(),
        open(os.path.join('docs', 'INSTALL.txt')).read(),
        open(os.path.join('docs', 'LICENSE.txt')).read(),
        open(os.path.join('docs', 'HISTORY.txt')).read(),
    ]),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Intended Audience :: Other Audience",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Zope",
    ],
    keywords='web zope plone theme',
    author='Thomas Massmann',
    author_email='thomas@propertyshelf.com',
    maintainer='Thomas Massmann',
    maintainer_email='thomas@propertyshelf.com',
    url='http://pypi.propertyshelf.com',
    download_url='http://pypi.python.org/pypi/customer.mlscrcom',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['customer'],
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'test': [
            'plone.app.testing',
        ]
    },
    install_requires=[
        'setuptools',
        'Plone',
        'plone.app.registry',
        'plone.app.theming',
        'plone.app.themingplugins',
    ],
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
