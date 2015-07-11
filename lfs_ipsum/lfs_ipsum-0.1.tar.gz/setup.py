# python imports
import os
from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
setup(name='lfs_ipsum',
    version='0.1',
    description='Content generator for LFS',
    long_description=README,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    keywords='django e-commerce online-shop lorem ipsum',
    author='Noe Nieto',
    author_email='nnieto@noenieto.com',
    url='http://github.com/tzicatl/lfs_ipsum',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'loremipsum'
    ],
)