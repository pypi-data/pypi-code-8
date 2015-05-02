import os

from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.rst')
    )

setup(
    name="sourceparse",
    version="0.2.5",
    description="utility to inspect python source codes",
    licence="MIT",
    author="Nicolas Laurance",
    author_email="nicolas[dot]laurance[at]gmail[dot]com",
    url="https://github.com/nlaurance/sourceparse",
    packages=find_packages(exclude=['ez_setup', 'tests']),
    zip_safe=False,
    include_package_data=True,
    tests_require=["nose"],
    test_suite='nose.collector',
    keywords=[
        'source code', 'analyzer'
    ],
    long_description=long_description,
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
    ],
)
