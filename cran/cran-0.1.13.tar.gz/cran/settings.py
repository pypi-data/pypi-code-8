from os.path import abspath, dirname, join
from os import environ

CRAN_ROOT = dirname(dirname(abspath(__file__)))
CRAN_LOCAL = join(environ['HOME'], '.cran')
CRAN_REPOS = 'https://github.com/lovestats/'
