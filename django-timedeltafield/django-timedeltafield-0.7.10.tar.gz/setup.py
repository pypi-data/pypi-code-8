import os.path
from setuptools import setup

setup(
    name="django-timedeltafield",
    version=open(os.path.join(os.path.dirname(__file__), 'timedelta', 'VERSION')).read().strip(),
    description="TimedeltaField for django models",
    long_description=open("README").read(),
    url="http://bitbucket.org/schinckel/django-timedelta-field/",
    author="Matthew Schinckel",
    author_email="matt@schinckel.net",
    packages=[
        "timedelta",
        "timedelta.templatetags",
    ],
    package_data={'timedelta': ['VERSION']},
    classifiers=[
        'Framework :: Django :: 1.4',
        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='tests.main',
)
