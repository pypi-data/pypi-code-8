from setuptools import setup
VERSION = '1.0.2'

setup(
    name='ma',
    version = VERSION,
    description='''Collection of tools and utilities. This is just a metapackage,
    which depends on all other ma.x packages''',
    author='Fredrik Haard',
    author_email='fredrik@metallapan.se',
    install_requires = ['ma.mongo==' + VERSION]
)
