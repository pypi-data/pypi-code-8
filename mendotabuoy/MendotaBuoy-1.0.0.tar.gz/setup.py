from setuptools import setup, find_packages

setup(
    name='MendotaBuoy',
    version='1.0.0',
    description='Mendota buoy l00 to a1 conversion.',
    url = 'http://metobs.ssec.wisc.edu',
    install_requires=[
    'numpy',
    'MetObsCommon>=0.1dev',
    ],

    packages = ['mendota-buoy']
)
