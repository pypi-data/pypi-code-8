import os
from setuptools import setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='google_oauthclient',
    version='2.3',
    packages=['google_oauthclient'],
    include_package_data=True,
    install_requires=['oauth2client','django-cors-headers'],
    license='MIT',
    description='',
    author='Evan Harris',
    url = 'https://github.com/harrise/django-oauthclient',
    download_url = 'https://github.com/harrise/django-oauthclient/tarball/2.3', 
    author_email='harrise@carleton.edu',
    classifiers=[
    ],
)
