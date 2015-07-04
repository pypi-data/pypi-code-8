from setuptools import find_packages
from setuptools import setup

VERSION='0.0.2'

setup(
    author='Alex Clark',
    author_email='aclark@aclark.net',
    classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Programming Language :: Python :: 2.7',
    ],
    description='Use dj-database-url to parse DATABASE_URL for Buildout environments',
    entry_points={
        'zc.buildout': 'default=collective.recipe.database_url:Recipe',
    },
    keywords='buildout database plone python url',
    license='Whatever Plone is',
    include_package_data=True,
    install_requires=[
        'dj-database-url',
        'setuptools',
    ],
    long_description=open('README.rst').read() + '\n' + open('CHANGES.rst').read(),
    name='collective.recipe.database_url',
    namespace_packages=[
        'collective',
        'collective.recipe',
    ],
    packages=find_packages(),
    test_suite='collective.recipe.database_url.tests.TestSuite',
    url='https://github.com/collective/collective.recipe.database_url',
    version=VERSION,
    zip_safe=False,
)
