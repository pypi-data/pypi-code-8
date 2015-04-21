# coding: utf-8
import fpstool
from setuptools import setup, find_packages

setup(
    name='fpstool',
    version=fpstool.__version__,
    license="MIT",
    description='get FPS for android',

    author='codeskyblue',
    author_email='codeskyblue@gmail.com',
    url='http://github.com/netease/unknown',

    packages = find_packages(),
    include_package_data=True,
    package_data={},
    install_requires=[
        'requests>=2.4.1',
        ],
    # entry_points='''
    #     [console_scripts]
    #     fpstool = pyfpstool:main
    # ''',
)
