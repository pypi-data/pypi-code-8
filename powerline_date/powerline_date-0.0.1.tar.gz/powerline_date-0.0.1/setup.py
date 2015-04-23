from setuptools import setup, find_packages
from powerline_date import version

setup(
    name='powerline_date',
    author='Colin Wood',
    author_email='cwood06@gmail.com',
    install_requires=[
        'python-dateutil',
    ],
    url='https://bitbucket.org/colinbits/powerline-date',
    download_url='https://bitbucket.org/colinbits/powerline-date',
    long_description=open('README.mkd').read(),
    version=version,
    include_package_data=True,
    packages=find_packages(),
    description='',
    tests_require=[
        'nose',
    ],
    keywords=[],
)
