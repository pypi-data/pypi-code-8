from os import environ
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read(environ["HOME"] + "/.mypy/myhelp/myhelp.cfg")
editor = config.get("Editor","path")
if not editor:
	print "Not Editor defined!"
	quit()
