# -*- coding: utf-8 -*-

# =============================================================
# Author: http://sefikail.cz
# =============================================================

import os
import errno
from random import choice
from shutil import rmtree
from tempfile import gettempdir


TMP_MAX = 10000

# @formatter:off (pycharm - no formatting)
characters = {
	'letters': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
	'digits': '0123456789'
}
# @formatter:on (pycharm - no formatting)

def generate_random_chain(length=12):
	all_chars = ''.join(str(x) for x in characters.values())  # All the characters in one variable
	rand_chars = ''.join(choice(all_chars) for x in range(length))  # Generate random characters
	return rand_chars


def TemporaryDirectory(suffix="", prefix="", dir=None, delete=True):
	if not dir or dir is None:
		dir = gettempdir()

	tempdir = os.path.join(dir, prefix + generate_random_chain() + suffix)
	for i in range(TMP_MAX, 0, -1):
		try:
			os.mkdir(tempdir)
		except OSError as e:
			if e.errno == errno.EEXIST:  # If folder exists, try again.
				tempdir = os.path.join(dir, prefix + generate_random_chain() + suffix)
			else:
				raise e
		else:
			return TemporaryDirectoryWrapper(tempdir, delete)
	raise Exception('Cannot create temp directory "%s".' % tempdir)


class TemporaryDirectoryWrapper:
	def __init__(self, tempdir, delete=True):
		self.tempdir = tempdir
		self.delete = delete
		self.rmtemp_called = False

		if not os.path.exists(tempdir):
			raise Exception('Cannot find temp directory "%s".' % tempdir)

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.rmtemp()

	def __del__(self):
		self.rmtemp()

	def rmtemp(self):
		if not self.rmtemp_called:
			self.rmtemp_called = True
			if self.delete and os.path.exists(self.tempdir):
				rmtree(self.tempdir)
				if os.path.exists(self.tempdir):
					raise Exception('Cannot remove temp directory "%s".' % self.tempdir)

	@property
	def name(self):
		return self.tempdir
