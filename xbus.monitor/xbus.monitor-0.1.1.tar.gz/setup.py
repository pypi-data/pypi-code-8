import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()

with open(os.path.join(here, 'CONTRIBUTORS.rst')) as f:
    CONTRIBUTORS = f.read()

requires = [
    'msgpack-python',
    'psycopg2',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_httpauth',
    'pyramid_redis_sessions',
    'pyramid_tm',
    'pyzmq',
    'redis',
    'six',
    'SQLAlchemy',
    'transaction',
    'waitress',
    'xbus.broker',
    'xbus.file_emitter',
    'zope.sqlalchemy',
]

setup(
    name='xbus.monitor',
    version='0.1.1',
    description='Xbus Monitor',
    long_description="{}\n{}\n{}".format(README, CONTRIBUTORS, CHANGES),
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='XCG',
    author_email='contact@xcg-consulting.fr',
    url='http://xbus.io',
    keywords='xbus monitor web pyramid',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='xbus.monitor',
    install_requires=requires,
    tests_require=requires,
    entry_points="""\
    [paste.app_factory]
    main = xbus.monitor:main
    """,
    message_extractors={'xbus.monitor': [
        ('xbus/monitor/**.py', 'lingua_python', None),
        ('xbus/monitor/templates/**.pt', 'lingua_xml', None),
    ]},
)
