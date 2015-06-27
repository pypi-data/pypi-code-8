# coding: utf-8

from setuptools import setup, find_packages

README = open('README.md').read()


setup(
    name='yufou',
    version='0.0.1',

    author='hbc',
    author_email='bcxxxxxx@gmail.com',
    url='https://github.com/bcho/yufou',

    description='Retrieve radar image.',
    long_description=README,
    license='MIT',

    packages=find_packages(exclude=['tests', 'data']),
    package_data={'': ['data/radar.json']},
    include_package_data=True,
    install_requires=[],
    extra_require={
        'test': ['pytest']
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ]
)
