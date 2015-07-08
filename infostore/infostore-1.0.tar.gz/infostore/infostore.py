import random
from cpfile import *
import sys, os, imp

class infobase():
	base = []
	def __init__(self, name, values=[]):
		self.name = name
		self.values = values 
	def __call__(self):
		return self.base
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
	def new(self):
		collums = ['Num', 'Name']
		base = [collums]
		for value in self.values:
			collums.append(value)
		write(os.path.dirname(os.path.realpath(__file__)) +'/storage/infobases.py', '''
class ''' + str(self.name) + '''():
	def __init__(self):
		pass
	def get(self):
		infobase = ''' + str(self.base) + '''
		return infobase''')
		self.base = base
	def show_infobases(self):
		return os.listdir(os.path.dirname(os.path.realpath(__file__)) +'/storage')
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
		write(os.path.dirname(os.path.realpath(__file__)) +'/storage/infobases.py', '''
class ''' + str(self.name).replace(' ', '_') + '''():
	def __init__(self):
		pass
	def get(self):
		infobase = ''' + str(self.base) + '''
		return infobase''')
	def load(self):
		checkdir('storage')
		self.base = load_from_file(os.path.dirname(os.path.realpath(__file__)) + '/storage/infobases.py', str(self.name).replace(' ', '_'))
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
	
class hierarchy():
	def __init__(self, Title, Basic_layout = []):
		self.title = Title
		self.b_layout = Basic_layout
	def __call__(self):
		try:
			return self.hierarchy
		except:
			return self.new()
	def save(self):
		checkdir("storage")
		write(os.path.dirname(os.path.realpath(__file__)) +'/storage/notesapp.py', '''
class ''' + str(self.title) + '''():
	def __init__(self):
		pass
	def get(self):
		hierarchy = ''' + str(self.hierarchy) + '''
		return hierarchy''')
	def load(self):
		checkdir('storage')
		self.hierarchy = load_from_file(os.path.dirname(os.path.realpath(__file__)) + '/storage/notesapp.py', str(self.title))
		self.hierarchy = self.hierarchy.get()
	def new(self, save = False):
		self.hierarchy = {}
		self.hierarchy[self.title] = {}
		for item in self.b_layout:
			self.hierarchy[self.title][item] = {}
		if bool(save):
			print 'Saving...'
			self.save()
		return self.hierarchy
	def search(self, path):
		self.pathlist = []
		self.pathlist.extend(path.split('/'))
		try:
			if len(self.pathlist) == 1:
				return self.hierarchy[self.pathlist[0]]
			elif len(self.pathlist) == 2:
				return self.hierarchy[self.pathlist[0]][self.pathlist[1]]
			elif len(self.pathlist) == 3:
				return self.hierarchy[self.pathlist[0]][self.pathlist[1]][self.pathlist[2]]
			elif len(self.pathlist) == 4:
				return self.hierarchy[self.pathlist[0]][self.pathlist[1]][self.pathlist[2]][self.pathlist[3]]
			elif len(self.pathlist) == 5:
				return self.hierarchy[self.pathlist[0]][self.pathlist[1]][self.pathlist[2]][self.pathlist[3]][self.pathlist[4]]
		except KeyError:
			return 'Error, Item not found'

class grid(object):
	def __init__(self, title, size = [10, 10]):
		self.title = title
		self.size = size
	def new(self):
		self.grid = []
		row = []
		for i in range(int(self.size[0])):
			row.append([])
			print row
		self.grid.append(row)
		for i in range(int(self.size[1]) - 1):
			self.grid.append(row)
		if self.size == 3:
			self.plane = [self.grid]
			self.grid = []
			for i in range(int(self.size[2])):
				self.grid.append(self.plane)
	def save(self):
		checkdir("storage")
		write(os.path.dirname(os.path.realpath(__file__)) +'/storage/grids.py', '''
class ''' + str(self.title) + '''():
	def __init__(self):
		pass
	def get(self):
		hierarchy = ''' + str(self.grid) + '''
		return hierarchy''')
	def load(self):
		checkdir('storage')
		self.grid = load_from_file(os.path.dirname(os.path.realpath(__file__)) + '/storage/grids.py', str(self.title))
		self.grid = self.hierarchy.get()

class point(object):
	def __init__(self, x, y, z, data = []):
		self.x = x
		self.y = y
		self.z = z
		self.data = data
	def __call__(self):
		return [self.x, self.y, self.z, self.data]

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
		print 'Error 404, Class instance Not Found'
		sys.exit()