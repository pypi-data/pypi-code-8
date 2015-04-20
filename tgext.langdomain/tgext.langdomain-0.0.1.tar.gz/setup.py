from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

version = "0.0.1"

testpkgs = [
    'WebTest == 1.4.3',
    'nose',
    'coverage',
    'tgext.pluggable'
]

setup(
    name='tgext.langdomain',
    version=version,
    description="TurboGears2 extension for detecting user language from the domain",
    long_description=README,
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='turbogears2.extension',
    author='AXANT',
    author_email='tech@axant.it',
    url='https://bitbucket.org/axant/tgext.langdomain',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['tgext'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "TurboGears2 >= 2.3.4",
    ],
    test_suite='nose.collector',
    tests_require=testpkgs,
    extras_require={
       # Used by Drone.io
       'testing': testpkgs,
    },
    entry_points="""
    # -*- Entry points: -*-
    """
)
