import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='djangofwd-news',
    version='0.1.3',
    packages=['news'],
    include_package_data=True,
    license='MIT',
    description='A simple Django app to conduct Web-based news.',
    long_description=README,
    url='http://www.fwd.hr/',
    author='Daniele Milani',
    author_email='daniele@fwd.hr',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
	keywords='News fwd development',
	install_requires = [
        'Django==1.6.11',
		'django-appconf==1.0.1',
		'django-bootstrap-form==3.2',
		'django-classy-tags==0.6.1',
		'django-cms==3.0.12',
		'django-jsonfield==0.9.13',
		'django-modeltranslation==0.8.1',
		'django-mptt==0.6.1',
		'django-sekizai==0.8.1',
		'django-user-accounts==1.0.1',
		'djangocms-admin-style==0.2.5',
		'djangocms-text-ckeditor==2.4.3',
		'easy-thumbnails==2.2',
		'eventlog==0.10.0',
		'html5lib==0.999',
		'metron==1.3.5',
		'MySQL-python==1.2.5',
		'Pillow==2.8.1',
		'pinax-theme-bootstrap==5.7.2',
		'pytz==2015.2',
		'six==1.9.0',
		'South==1.0.2',
		'yolk==0.4.3',
    ],
)