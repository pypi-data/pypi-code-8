"""A CLI toolbelt for SpikeNode PaaS.

See:
https://github.com/spikenode/toolbelt
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst')) as f:
    long_description = f.read()

setup(
    name='spikenode',
    version='0.1.3',
    description='SpikeNode Toolbelt',
    long_description=long_description,
    url='https://github.com/spikenode/toolbelt',
    author='Allan Denot',
    author_email='allan.denot@spikenode.com',
    license='MIT',
    py_modules=['spikenode'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='spikenode devops ansible',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
      'requests>=2.7.0',
      'pyopenssl',
      'ndg-httpsclient',
      'pyasn1',
      'urllib3',
    ],
    entry_points={
        'console_scripts': [
            'spikenode=spikenode:main',
        ],
    },
)
