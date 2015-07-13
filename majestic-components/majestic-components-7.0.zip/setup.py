from distutils.core import setup
setup(
  name = 'majestic-components',
  packages = ['majestic-components'], # this must be the same as the name above
  package_data={'majestic-components': ['*.jpg', '*.png', '*.mp4']},
  version = '7.0',
  description = 'Components For Majestic Pi',
  author = 'Matthew Swallow',
  author_email = 'mrobraven@gmail.com',
  url = 'https://github.com/mrobraven/majestic-pi', # use the URL to the github repo
  download_url = 'https://github.com/mrobraven/majestic-pi/tarball/7.0', # I'll explain this in a second
  keywords = ['cinema', 'theatre', 'home'], # arbitrary keywords
  classifiers = [],
)
