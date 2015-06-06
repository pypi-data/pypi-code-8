from setuptools import setup

setup(
    name='ma',
    version = '1.0.0',
    description='''Collection of tools and utilities. This is just a metapackage,
    which depends on all other ma.x packages''',
    author='Fredrik Haard',
    author_email='fredrik@metallapan.se',
    install_requires = ['ma.mongo==1.0.0']
)
