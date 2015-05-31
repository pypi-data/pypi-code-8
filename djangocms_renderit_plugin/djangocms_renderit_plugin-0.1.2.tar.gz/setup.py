from distutils.core import setup
from setuptools import find_packages

setup(
    name = 'djangocms_renderit_plugin',
    include_package_data=True,
    version = '0.1.2',
    description = 'Use Django templating language in DjangoCMS plugins.',
    author = 'frnhr',
    author_email = 'frnhr@changeset.hr',
    url = 'https://github.com/frnhr/djangocms_renderit', # use the URL to the github repo
    download_url = 'https://github.com/frnhr/djangocms_renderit/tarball/0.1', # I'll explain this in a second
    keywords = ['djangocms', 'django-template'], # arbitrary keywords
    classifiers = [],
)
