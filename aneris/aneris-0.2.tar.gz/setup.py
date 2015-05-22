#!/usr/bin/python3

from distutils.core import setup

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945

import codecs
try:
	codecs.lookup('mbcs')
except LookupError:
	ascii = codecs.lookup('ascii')
	func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
	codecs.register(func)

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

setup(
	name = "aneris",
	packages = ["aneris"],
	version = "0.2",
	description = "curses time/project planner",
	author = "the_night_penguin",
	author_email = "of.many.devices@gmail.com",
	url = "http://pypi.python.org/pypi/aneris",
	keywords = ["time", "project", "planning"],
	classifiers = [
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Development Status :: 3 - Alpha",
		"Environment :: Other Environment",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
		"Operating System :: OS Independent",
		"Topic :: Office/Business :: Scheduling",
	],
)
