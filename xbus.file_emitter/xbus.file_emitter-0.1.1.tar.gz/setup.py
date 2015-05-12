import os
from setuptools import find_packages
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()

with open(os.path.join(here, 'CONTRIBUTORS.rst')) as f:
    CONTRIBUTORS = f.read()


requires = [
    'msgpack-python',
    'pyjon.descriptors',
    'pyzmq',
]


setup(
    name='xbus.file_emitter',
    version='0.1.1',
    description='Generic Xbus file emitter.',
    long_description="{}\n{}\n{}".format(README, CONTRIBUTORS, CHANGES),
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
    ],
    author='XCG',
    author_email='contact@xcg-consulting.fr',
    url='http://xbus.io',
    keywords='xbus file emitter',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    test_suite='xbus.file_emitter',
)
