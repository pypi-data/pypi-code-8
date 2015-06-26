
from setuptools import setup, find_packages
import sys, os

version = '1.0'

setup(
    name = 'funcomp',
    version = version,
    description = "Function composition is simple.",
    packages = find_packages( exclude = [ 'ez_setup'] ),
    include_package_data = True,
    zip_safe = False,
    entry_points = {},
    author = 'Bence Faludi',
    author_email = 'bence@ozmo.hu',
    license = 'GPL',
    install_requires = [],
    test_suite = "funcomp.tests"
)
