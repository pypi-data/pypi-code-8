VERSION = '0.0.2a1'

from setuptools import setup, find_packages

setup(
    name='nagare-jquery',
    version=VERSION,
    author='',
    author_email='herve.coatanhay@gmail.com',
    description='Nagare renderer that uses jquery as async backend',
    long_description=open('README.rst', 'r').read(),
    keywords='',
    url='https://github.com/Alzakath/nagare-jquery',
    packages=find_packages(),
    license='',
    include_package_data=True,
    zip_safe=False,
    install_requires=('nagare',),
    namespace_packages=('nagare', 'nagare.contrib', ),
)
