import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

install_requires = [
    'bowerstatic',
    'pyramid',
    'zope.interface',
]

tests_require = [
    'nose',
    'pyramid_chameleon',
    'webtest',
]


setup(
    name='djed.static',
    version='0.4',
    description='Integration of BowerStatic into Pyramid for managing '
                'static resources with Bower',
    long_description='\n\n'.join([README, CHANGES]),
    classifiers=[
        "Framework :: Pyramid",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet :: WWW/HTTP",
    ],
    author='Djed developers',
    author_email='djedproject@googlegroups.com',
    url='https://github.com/djedproject/djed.static',
    license='ISC License (ISCL)',
    keywords='djed pyramid pylons bower static bowerstatic',
    packages=['djed.static'],
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'testing': tests_require,
    },
    test_suite='nose.collector',
)
