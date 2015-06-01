import random
from cpfile import *
import sys, os, imp

class infobase(object):
	base = []
	def __init__(self, name, values=[]):
		self.name = name
		self.values = values
	def __str__(self):
		ptable = self.base
		prt = ptable
		divider = []
		col_width = [max(len(str(x)) for x in col) for col in zip(*prt)]
		i = 0
		for value in col_width:
			dash = (''.join('-' for a in range(col_width[i])))
			divider.append(dash)
			i += 1
		prt.insert(1, divider)
		print ''
		for line in prt:
			print "| " + " | ".join("{:{}}".format(x, col_width[i])
									for i, x in enumerate(line)) + " |"
		self.base.remove(self.base[1])
		return ''
	def __repr__(self):
		return str(self.base)
	def new_infobase(self):
		collums = ['Num', 'Name']
		base = [collums]
		for value in self.values:
			collums.append(value)
		print('Storing infobase in file')
		write(os.path.dirname(os.path.realpath(__file__)) +'/infobases/storage.py', '''
class ''' + str(self.name) + '''():
	def __init__(self):
		pass
	def get(self):
		infobase = ''' + str(self.base) + '''
		return infobase''')
		self.base = base
	def show_infobases(self):
		return os.listdir(os.path.dirname(os.path.realpath(__file__)) +'/infobases')
	def add_row(self, content):
		toadd = [len(self.base)]
		toadd.extend(content)
		self.base.append(toadd)
	def remove_row(self, n=None):
		if n != 1:
			n = int(n)
			self.base.pop(n)
		else:
			self.base.pop()
	def save(self):
		print('Storing infobase in file')
		write(os.path.dirname(os.path.realpath(__file__)) +'/infobases/storage.py', '''
class ''' + str(self.name) + '''():
	def __init__(self):
		pass
	def get(self):
		infobase = ''' + str(self.base) + '''
		return infobase''')
	def load(self):
		checkdir('infobases')
		self.base = load_from_file(os.path.dirname(os.path.realpath(__file__)) + '/infobases/storage.py', str(self.name))
		self.base = self.base.get()
	def itemsbycollum(self, collum=1, num=-1):
		self.collums = zip(*self.base)
		return str(self.collums[collum][0]), self.collums[collum][num]
	def getvalue(self, collum=1, num=-1):
		items = self.itemsbycollum(collum, num)
		return items[0] + ' : ' + items[1]
	def repvalue(self, torep, repwith):
		self.base[torep[0]][torep[1]] = repwith
	def rmval(self, value):
		repvalue(value, 'None')


def load_from_file(filepath, ctf):
	try:
	    class_inst = None
	    expected_class = ctf
	    mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])
	    if file_ext.lower() == '.py':
	        py_mod = imp.load_source(mod_name, filepath)
	    elif file_ext.lower() == '.pyc':
	        py_mod = imp.load_compiled(mod_name, filepath)
	    if hasattr(py_mod, expected_class):
	        class_inst = getattr(py_mod, expected_class)()
	    return class_inst
	except IOError:
		print 'Error 404, Infobase Not Found'
		sys.exit()