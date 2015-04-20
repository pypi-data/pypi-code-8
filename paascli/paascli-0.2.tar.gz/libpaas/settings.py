__author__ = 'hvishwanath'

import os

cliroot = os.path.join(os.path.expanduser("~"), ".paas")
if not os.path.isdir(cliroot):
    os.makedirs(cliroot)

cfgfile = os.path.join(cliroot, '.paascli.yaml')
dbfile = os.path.join(cliroot, 'paascli.sqlite3')


