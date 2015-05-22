from distutils.core import setup
setup(
  name = 'HeyNicePackage',
  packages = ['HeyNicePackage'], # this must be the same as the name above
  version = '0.1',
  description = 'A random test lib',
  author = 'Tristan Sweeney',
  author_email = 'sweeney.tr@husky.neu.edu',
  url = 'https://github.com/sweeneytr/HeyNicePackage', # use the URL to the github repo
   #@download_url
   #Link to repository code. 
   #In git repository, run ( git tag {version} -m "Commit to put on PyPI" )
   #run ( git tag ) to confirm {version} is in the list
   #run ( git push --tags origin master ) to update tags
   # After this, git creates tarballs for download at https://github.com/{username}
   #                                                   /{module_name}/tarball/{tag}
  download_url = 'https://github.com/sweeneytr/HeyNicePackage/tarball/0.1',
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
)
