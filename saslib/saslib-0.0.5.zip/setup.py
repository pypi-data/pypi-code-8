import sys
from distutils.core import setup

if sys.version_info < (2, 6):
    print("Sorry, this module only works on 2.6+, 3+")
    sys.exit(1)

setup(name='saslib',
      packages = ['saslib'],
      version ='0.0.5',
      author = 'chao huang',
      author_email = 'hchao8@gmail.com',
      license = 'MIT',
      url =' https://github.com/dapangmao/saslib',
      description = 'An HTML report generator to perform the meta data lookup like PROC CONTENTS in SAS',
      requires = ['sas7bdat', 'jinja2'],
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 3',
          'Topic :: Text Processing',
          'Topic :: Utilities',
      ],
      keywords = ['sas', 'sas7bdat', 'html']
 )
