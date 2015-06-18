from distutils.core import setup
setup(
  name = 'bib2web',
  packages = ['bib2web', 'bib2web.bibtexparser'], # this must be the same as the name above
  version = '0.17',
  description = 'Reference manager and generate website with it using BibBase.org',
  author = 'Justin van Wageningen',
  author_email = 'justinvwageningen@gmail.com',
  url = 'https://github.com/Juvawa/bib2web', # use the URL to the github repo
  download_url = 'https://github.com/Juvawa/bib2web/tarball/0.17', # I'll explain this in a second
  keywords = ['bibtex', 'BibBase', 'Universiteit van Amsterdam'], # arbitrary keywords
  classifiers = [],
  install_requires = ['pybtex==0.18', 'fuzzywuzzy==0.5.0', 'latexcodec==1.0.1'],
)