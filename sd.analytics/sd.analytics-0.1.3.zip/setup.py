from setuptools import find_packages
from setuptools import setup

version = '0.1.3'

setup(
    name='sd.analytics',
    version=version,
    description="Google analytics integration for Singing & Dancing",
    long_description='\n'.join([
        open("README.rst").read(),
        open("HISTORY.rst").read(),
        ]),
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        ],
    keywords='google analytics singing dancing newsletter trackingaddon extension',
    author='Thomas Clement Mogensen',
    author_email='thomas@headnet.dk',
    url='http://www.headnet.dk',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['sd'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'collective.dancing',
        # -*- Extra requirements: -*-
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
    )
