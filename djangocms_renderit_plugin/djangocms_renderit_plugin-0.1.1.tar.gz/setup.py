from distutils.core import setup
setup(
    name = 'djangocms_renderit_plugin',
    packages = ['djangocms_renderit_plugin'], # this must be the same as the name above
    version = '0.1.1',
    description = 'Use Django templating language in DjangoCMS plugins.',
    author = 'frnhr',
    author_email = 'frnhr@changeset.hr',
    url = 'https://github.com/frnhr/djangocms_renderit', # use the URL to the github repo
    download_url = 'https://github.com/frnhr/djangocms_renderit/tarball/0.1', # I'll explain this in a second
    keywords = ['djangocms', 'django-template'], # arbitrary keywords
    classifiers = [],
)
