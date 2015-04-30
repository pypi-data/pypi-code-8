from setuptools import setup
setup(
      name = 'broffeact',
      packages = ['broffeact'], # this must be the same as the name above
      version = '0.2.1',
      description = 'A simple brunch/coffeescript/reactjs documentation generator',
      author = 'Yves Lange',
      author_email = 'kursion@gmail.com',
      url = 'https://github.com/kursion/broffeact', # use the URL to the github repo
      # download_url = 'https://github.com/peterldowns/mypackage/tarball/0.1', # I'll explain this in a second
      keywords = ['coffeescript', 'documentation', 'generator', 'reactjs', 'brunch'], # arbitrary keywords
      classifiers = [],
      zip_safe=False,
      entry_points={'console_scripts': [
          'broffeact = broffeact.__init__:main'
      ]}
)
