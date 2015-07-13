import sys
from setuptools import setup, find_packages

setup(
    name='imhotep_eslint',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/justinabrahms/imhotep_eslint',
    license='MIT',
    install_requires=['imhotep>=0.4.0'],
    tests_require=['mock', 'pytest'],
    author='Justin Abrahms',
    author_email='justin@abrah.ms',
    description='An imhotep plugin for eslint',
    entry_points={
        'imhotep_linters': [
            '.js = imhotep_eslint.plugin:ESLint'
        ],
    },
)
