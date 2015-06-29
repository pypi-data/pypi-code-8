from distutils.core import setup
from setuptools import find_packages

# execfile('blarf/version.py')

exec(open('blarf/version.py').read())

setup(
    name='blarf',
    version=__version__,
    packages=find_packages(),
    url='',
    license='',
    author='rtuin',
    author_email='richard@newnative.nl',
    description='',
    entry_points={
        'console_scripts': ['blarf=blarf:console']
    }
)
