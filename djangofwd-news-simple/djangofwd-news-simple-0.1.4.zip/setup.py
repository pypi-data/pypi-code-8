import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='djangofwd-news-simple',
    version='0.1.4',
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
	keywords='News fwd simple development',
	install_requires = [
		'django-classy-tags==0.6.1',
		'django-modeltranslation==0.8.1',
		'easy-thumbnails==2.2',
		'Pillow==2.8.1',
		'pytz==2015.2',
    ],
)