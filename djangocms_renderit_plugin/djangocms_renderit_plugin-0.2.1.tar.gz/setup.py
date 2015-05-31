from distutils.core import setup
from setuptools import find_packages


VERSION = "0.2.1"

packages = find_packages(exclude=('publish_utils',))
packages = list(filter(lambda file: "publish_utils" not in file, packages))

setup(
    name = 'djangocms_renderit_plugin',
    include_package_data = True,
    packages = packages,
    version = VERSION,
    description = 'Use Django templating language in DjangoCMS plugins.',
    author = 'frnhr',
    author_email = 'frnhr@changeset.hr',
    url = 'https://github.com/frnhr/djangocms_renderit', # use the URL to the github repo
    download_url = 'https://github.com/frnhr/djangocms_renderit/tarball/0.1', # I'll explain this in a second
    keywords = ['djangocms', 'django-template'], # arbitrary keywords
    classifiers = [],
)
