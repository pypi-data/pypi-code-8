import re
from setuptools import setup, find_packages

packages = find_packages('.', exclude=('tests', 'tests.*'))

install_requires = [
    'certifi',
    'iso8601',
    'paramiko >= 1.0,<2.0',
]

extras_require = {
    'tests': [
        'pytest >=2.5.2,<3',
        'pytest-cov >=1.7,<2',
    ],
}

setup(
    name='mythical',
    version=(
        re
        .compile(r".*__version__ = '(.*?)'", re.S)
        .match(open('mythical/__init__.py').read())
        .group(1)
    ),
    url='https://github.com/verygoodgroup/mythical-client',
    author='Franz Sanchez',
    author_email='dev+mythical@vgs.io',
    description='Mythical client',
    long_description=open('README.rst').read(),
    platforms='any',
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require=extras_require,
    tests_require=extras_require['tests'],
    packages=packages,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='nose.collector',
)
