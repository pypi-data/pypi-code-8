__author__ = 'Tom James Holub'

import threading


def delegate(callback, args_list=None, args_dict=None):
	delegator = FunctionDelegator(callback, args_list or [], args_dict or {})
	delegator.start()


class FunctionDelegator(threading.Thread):

	def __init__(self, callback, args_list, args_dict):
		threading.Thread.__init__(self)
		self.cb = callback
		self.list = args_list
		self.dict = args_dict

	def run(self):
		self.cb(*self.list, **self.dict)