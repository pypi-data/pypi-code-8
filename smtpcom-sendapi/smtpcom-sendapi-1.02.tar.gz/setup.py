#!/usr/bin/python

from setuptools import setup, find_packages

RELEASE = '1'

setup(
    name = "smtpcom-sendapi",
    version="1.02",
#    release = RELEASE,
    author = "Yana",
    author_email = "yana@smtp.com",
    maintainer = "Yand Kornienko",
    maintainer_email = "yana@smtp.com",
    description = "SMTP SendApi",
    url = 'http://smtp.com/',
    license='Copyright 2015, SMTP.COM.',
    setup_requires=["nose>=1.0"],
    install_requires = [
        "PyYAML==3.10",
        "requests",
        "distribute==0.7.3"
    ],
    tests_require = [
        "mock==1.0.1",
        "coverage==3.7.1",
        "nose==1.3.0",
        "nose-cover3==0.1.0",
    ],
    packages = find_packages(where='lib'),  # include all packages under lib/
    package_dir = {'': 'lib', 'test': 'tests'},   # tell distutils packages are under src
    scripts = [],
    test_suite='tests',
    include_package_data = True,
    package_data = {
        '': ['*.yaml']
    },
    zip_safe=True,
)
