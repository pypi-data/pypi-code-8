import re
import setuptools


version = (
    re
    .compile(r".*__version__ = '(.*?)'", re.S)
    .match(open('mythicals/__init__.py').read())
    .group(1)
)

packages = setuptools.find_packages('.', exclude=('tests', 'tests.*'))

install_requires = [
    'iso8601 >=0.1.10,<0.2',
    'psycopg2 >=2.5.2,<3.0',
    'SQLAlchemy >=0.9,<=0.9.8',
    'sqlalchemy-pilo >=0.9.2,<0.10',
    'alembic >=0.6.4,<0.7',
    'pilo >=0.4,<0.5',
    'Flask >=0.10.1,<0.11',
    'netaddr >=0.7.11,<0.8',
    'boto >=2.29,<3.0',
    'flask-hype >=0.1.4,<0.2',
    'wsgim-rip >=0.1,<0.2',
    'wsgim-record >=0.1,<0.2',
    'fs >=0.5,<0.6',
    'paramiko >=1.0,<2.0',
    'coid >=0.1,<0.2',
    'newrelic >=2.28.0.26,<3.0',
    'ohmr >=0.1,<0.2',
    'pwho >=0.1,<0.2',
]

extras_require = {
    'daemon': [
        'cython >=0.20.1,<0.21',
        'gevent >=1.0,<2.0',
        'gunicorn >=19.1.1,<20.0',
        'setproctitle >=1.1,<2.0',
    ],
    'tests': [
        'nose >=1.0,<2.0',
        'jsonschema >=2.0,<3.0',
        'requests',
    ],
}

scripts = [
    'bin/mythicals',
    'bin/mythicald',
]

data_files = [
    # db
    (
        'mythicals/db',
        [
            'extras/db/role.py',
            'extras/db/create.py',
            'extras/db/alembic.ini'
        ]
    ),
    (
        'mythicals/db/alembic',
        [
            'extras/db/alembic/env.py',
            'extras/db/alembic/README'
        ]
    ),
    (
        'mythicals/db/alembic/versions',
        setuptools.findall('extras/db/alembic/versions')
    ),
]

setuptools.setup(
    name='mythicals',
    version=(
        re
        .compile(r".*__version__ = '(.*?)'", re.S)
        .match(open('mythicals/__init__.py').read())
        .group(1)
    ),
    url='https://github.com/verygood/mythical',
    author='Franz Sanchez',
    author_email='dev+mythical@vgs.io',
    description='',
    long_description='',
    platforms='any',
    include_package_data=True,
    install_requires=install_requires,
    extras_require=extras_require,
    tests_require=extras_require['tests'],
    packages=packages,
    scripts=scripts,
    data_files=data_files,
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
