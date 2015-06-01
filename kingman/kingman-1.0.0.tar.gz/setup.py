#
# Copyright (C) 2015 Jerome Kelleher <jerome.kelleher@well.ox.ac.uk>
#
# This file is part of kingman.
#
# kingman is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kingman is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kingman.  If not, see <http://www.gnu.org/licenses/>.
#
import re

# First, we try to use setuptools. If it's not available locally,
# we fall back on ez_setup.
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


# Following the recommendations of PEP 396 we parse the version number
# out of the module.
def parse_version(module_file):
    """
    Parses the version string from the specified file.

    This implementation is ugly, but there doesn't seem to be a good way
    to do this in general at the moment.
    """
    f = open(module_file)
    s = f.read()
    f.close()
    match = re.findall("__version__ = '([^']+)'", s)
    return match[0]

f = open("README.txt")
kingman_readme = f.read()
f.close()
kingman_version = parse_version("kingman/__init__.py")

setup(
    name="kingman",
    version=kingman_version,
    description="An example Python package to simulate Kingman's coalescent",
    long_description=kingman_readme,
    packages=["kingman"],
    author="Jerome Kelleher",
    author_email="jerome.kelleher@well.ox.ac.uk",
    url="http://pypi.python.org/pypi/kingman",
    entry_points={
        'console_scripts': [
            'kingman=kingman.cli:main',
        ]
    },
    install_requires=[],
    keywords=["Coalescent simulation", "Python packaging"],
    license="GNU GPLv3+",
    platforms=["POSIX"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Science/Research",
        (
            "License :: OSI Approved :: GNU General Public License "
            "v3 or later (GPLv3+)"
        ),
        "Operating System :: POSIX",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
)
