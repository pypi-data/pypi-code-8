"""Setuptools entry point."""
import codecs
import os.path
from setuptools import setup, find_packages

install_requires = [
    'kallithea',
    'requests-oauthlib',
]

long_description = []

for text_file in ['README.rst', 'CHANGES.rst']:
    with codecs.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), text_file), encoding='utf-8') as f:
        long_description.append(f.read())

setup(
    name="kallithea-auth-google",
    description="Kallithea google auth plugin",
    long_description="\n".join(long_description),
    author="Anatoly Bubenkov, Paylogic International and others",
    license="MIT license",
    author_email="developers@paylogic.com",
    url="https://github.com/paylogic/kallithea-google-auth",
    version="1.0.2",
    packages=find_packages(include="kallithea_auth_google*"),
    install_requires=install_requires,
    entry_points="""
    [paste.filter_app_factory]
    google-auth = kallithea_auth_google.middleware:make_middleware
    """
)
