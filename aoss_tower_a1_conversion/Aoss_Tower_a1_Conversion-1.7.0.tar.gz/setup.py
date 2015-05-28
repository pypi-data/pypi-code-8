from setuptools import setup, find_packages

setup(
    name= 'Aoss_Tower_a1_Conversion',
    version='1.7.0',
    description='convert AossTower ascii files to netCDF files',
    url='http://metobs.ssec.wisc.edu',
    install_requires=[
        'numpy',
        'MetObsCommon>=0.1dev',
	'AossTower'
    ],
    
    packages=['convertFromASCIIToNETCDF', 'convertFromASCIIToNETCDF.test'],
    #long_description=open('README.txt.read()'),
    #dependency_links=['http://larch.ssec.wisc.edu/cgi-bin/repos.cgi'],
    #packages=find_packages(exclude=['aosstower.tests']),
    #include_package_data=True,
)
