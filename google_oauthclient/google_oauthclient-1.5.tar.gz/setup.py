import os
from setuptools import setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='google_oauthclient',
    version='1.5',
    packages=['google_oauthclient'],
    include_package_data=True,
    license='MIT',
    description='',
    author='Evan Harris',
    url = 'https://github.com/harrise/django-oauthclient',
    download_url = 'https://github.com/harrise/django-oauthclient/tarball/1.5', 
    author_email='harrise@carleton.edu',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
