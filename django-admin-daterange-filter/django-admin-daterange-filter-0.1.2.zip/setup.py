import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-admin-daterange-filter',
    version='0.1.2',
    packages=['admin_daterange_filter'],
    zip_safe=False,
    include_package_data=True,
    license='BSD License',  # example license
    description='daterange-filter for django admin used by jquery.datepicker',
    long_description=README,
    url='https://github.com/nieoding/django-admin-daterange-filter',
    author='nieo ding',
    author_email='dingzh@66wifi.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)