from nose.tools import eq_
import sefara
from sefara import commands
from . import data_path

# currently unimplemented

def Xtest_dump():
    commands.dump.run([data_path("ex1.py")])

def Xtest_select():
    commands.select.run([data_path("ex1.py")])

def Xtest_check():
    commands.check.run([data_path("ex1.py")])


