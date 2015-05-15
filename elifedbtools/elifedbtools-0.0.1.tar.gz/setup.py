from setuptools import setup

import elifedbtools

with open('README.rst') as fp:
    readme = fp.read()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(name='elifedbtools',
    version=elifedbtools.__version__,
    description='Tools for article and production data storage',
    long_description=readme,
    packages=['elifedbtools'],
    license = 'MIT',
    install_requires=install_requires,
    url='https://github.com/elifesciences/elife-db-tools',
    maintainer='eLife Sciences Publications Ltd.',
    maintainer_email='py@elifesciences.org',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        ],
    )
