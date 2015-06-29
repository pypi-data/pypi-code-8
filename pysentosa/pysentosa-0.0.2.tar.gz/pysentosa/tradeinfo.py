__author__ = 'Wu Fuheng'
import config
import os

account = config.yml_sentosa['global']['account']
fpath = config.yml_sentosa['linux']['TRADEINFODIR'] + os.sep + account
print fpath
print config.SYMBOLS


