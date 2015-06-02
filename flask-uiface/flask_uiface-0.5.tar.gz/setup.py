from distutils.core import setup
setup(
  name = 'flask_uiface',
  packages = ['flask_uiface'], # this must be the same as the name above
  version = '0.5',
  install_requires=['json','requests'],
  description = 'Random user avatars for the rest of us!',
  author = 'Henri Kuiper',
  author_email = 'henrikuiper@zdevops.com',
  url = 'https://github.com/zdevops/flask-uiface', # use the URL to the github repo
  download_url = 'https://github.com/zdevops/flask-uiface', # I'll explain this in a second
  keywords = ['flask', 'avatar', 'uifaces'], # arbitrary keywords
  classifiers = [],
)
