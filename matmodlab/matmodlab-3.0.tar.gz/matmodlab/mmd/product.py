import os
import sys
import argparse
import ConfigParser
from distutils.spawn import find_executable as which
from os.path import join, dirname, realpath, isdir, isfile, expanduser


# ------------------------------------------------ PROJECT WIDE CONSTANTS --- #
VERSION = (2, 1, 0)

PLATFORM = sys.platform
PYEXE = realpath(sys.executable)

ROOT_D = dirname(dirname(realpath(__file__)))
MMD_D = join(ROOT_D, "mmd")
assert isdir(MMD_D)
VIZ_D = join(ROOT_D, "viz")
UTL_D = join(ROOT_D, "utils")
BIN_D = join(ROOT_D, "bin")
TEST_D = join(ROOT_D, "tests")
PKG_D = join(ROOT_D, "lib")
LIB_D = join(ROOT_D, "lib")
MAT_D = join(ROOT_D, "materials")
BLD_D = join(LIB_D, "build")

# These are the standard outputs, any other requests are output as text
DB_FMTS = ('exo', 'dbx', 'txt', 'pkl', 'xls', 'xlsx')

# --- OUTPUT DATABASE FILE
F_EVALDB = "mml-evaldb.xml"
F_PRODUCT = "product.py"

# --- MATERIAL AND TEST SEARCH DIRECTORIES
MAT_LIB_DIRS = [MAT_D]
TEST_DIRS = [join(TEST_D, __d) for __d in os.listdir(TEST_D)
             if isdir(join(TEST_D, __d))]

# User configuration
f = "matmodlabrc"
if isfile(f):
    RCFILE = realpath(f)
else:
    RCFILE = os.getenv("MATMODLABRC") or expanduser("~/.{0}".format(f))
p = argparse.ArgumentParser(add_help=False)
p.add_argument("-E", action="store_true", default=False)
_a, sys.argv[1:] = p.parse_known_args()
SUPPRESS_USER_ENV = _a.E

# OTHER CONSTANTS
TEST_CONS_WIDTH = 80

FFLAGS = [x for x in os.getenv("FFLAGS", "").split() if x.split()]
FC = which(os.getenv("FC", "gfortran"))

SPLASH = """\
                  M           M    M           M    L
                 M M       M M    M M       M M    L
                M   M   M   M    M   M   M   M    L
               M     M     M    M     M     M    L
              M           M    M           M    L
             M           M    M           M    L
            M           M    M           M    L
           M           M    M           M    LLLLLLLLL
                     Material Model Laboratory v {0}

""".format(".".join("{0}".format(i) for i in VERSION))
