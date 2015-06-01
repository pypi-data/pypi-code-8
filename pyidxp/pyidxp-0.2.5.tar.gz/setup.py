from setuptools import setup, find_packages

setup(
    name='pyidxp',
    version='0.2.5',
    author='Artur Rodrigues, Denis Lins',
    author_email='arturhoo@gmail.com, denis.lins@outlook.com',
    description='pyidxp - simple libs for our everyday needs',
    url='https://github.com/idxp/pyidxp',
    download_url='https://github.com/idxp/pyidxp/tarball/0.2.1',
    license='LICENSE',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'boto >= 2.36',
        'python-consul >= 0.3.19'
    ],
    tests_require=['pytest'],
)
