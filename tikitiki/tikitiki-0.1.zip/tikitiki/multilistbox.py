try:
	import Tkinter as tk
except:
	import tkinter as tk

'''
Multi-column listbox widget

based on Juan Ramirez activestate recipe 578805 updated to python 3.x

usage: 	lists can be a list of 3-tuples each denoting a column with 
		( Title, Width, Stickie )

TODO: Use draggable PanedWindow not Frames, see activestate recipe 52266 comments
'''
class MultiListbox(tk.Frame):
	def __init__(self, master, lists, **config):
		tk.Frame.__init__(self, master)
		self.lists = []
		for col_name,col_width,col_stickie in lists:
			expand = tk.NO if col_stickie else tk.YES
			frame = tk.Frame(self); frame.pack(side=tk.LEFT, expand=expand, fill=tk.BOTH)
			tk.Label(frame, text=col_name, borderwidth=1, relief=tk.RAISED).pack(fill=tk.X)
			lb = tk.Listbox(frame, width=col_width, 
				borderwidth=0, selectborderwidth=0, 
				relief=tk.FLAT, exportselection=tk.FALSE, takefocus=False)
			lb.configure(**config)
			lb.pack(expand=tk.YES, fill=tk.BOTH)
			self.lists.append(lb)
			lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
			lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
			lb.bind('<Leave>', lambda e: 'break')
			lb.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
			lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
			lb.bind('<Up>', lambda e, s=self: s._rowselect(s.curselection(), True))
			lb.bind('<Down>', lambda e, s=self: s._rowselect(s.curselection(), False))
		self.configure(takefocus=True)
		self.bind('<Up>', lambda e, s=self: s._rowselect(s.curselection(), True))
		self.bind('<Down>', lambda e, s=self: s._rowselect(s.curselection(), False))
		self.bind('<Prior>', lambda e, s=self: s._rowdrop(s.curselection(), True))
		self.bind('<Next>', lambda e, s=self: s._rowdrop(s.curselection(), False))
		
		frame = tk.Frame(self); frame.pack(side=tk.LEFT, fill=tk.Y)
		tk.Label(frame, borderwidth=1, relief=tk.RAISED).pack(fill=tk.X)
		sb = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self._scroll)
		sb.pack(expand=tk.YES, fill=tk.Y)
		self.lists[0]['yscrollcommand']=sb.set


	def addBinding(self, binding, cmd):
		self.bind(binding, cmd)
		for l in self.lists:
			l.bind(binding, cmd)

	def _rowdrop(self, index, up):
		# get current selected viewport pixel location
		cur_y = None
		index = self.curselection()
		if len(index) > 0:
			cur_y = self.lists[0].bbox(index)[1]

		if up:
			direction = -1
		else:
			direction = 1

		for l in self.lists:
			l.yview_scroll(direction, 'pages')
		
		# update the selected element is in the viewport, 
		if cur_y is not None:
			self._select( cur_y)
		
		# get the number of elements on view,
		page = 0

		# +/- this page number
		if len(index)>0:

			if up:
				index = index[0] - page
			else:
				index = index[0] + page

		else:
			index = 0

		return 'break'

	def _rowselect(self, index, up):

		if len(index)>0:

			if up:
				index = index[0] - 1
			else:
				index = index[0] + 1

		else:
			index = 0

		if index>=0 and index<self.lists[0].size():
			self.selection_clear(0, tk.END)
			self.selection_set(index)
			self.see(index)

		return 'break'

	def _select(self, y):
		row = self.lists[0].nearest(y)
		self.selection_clear(0, tk.END)
		self.selection_set(row)
		self.focus_force()
		return 'break'

	def _button2(self, x, y):
		for l in self.lists: l.scan_mark(x, y)
		return 'break'

	def _b2motion(self, x, y):
		for l in self.lists: l.scan_dragto(x, y)
		return 'break'

	def _scroll(self, *args):
		for l in self.lists:
			l.yview( *args )

	def curselection(self):
		return self.lists[0].curselection()

	def delete(self, first, last=None):
		for l in self.lists:
			l.delete(first, last)

	def enable(self):
		for l in self.lists:
			l.configure(state=tk.NORMAL)

	def get(self, first, last=None):
		result = []
		for l in self.lists:
			result.append(l.get(first,last))
		if last: 
			return map( None, *result)
		return result
		
	def index(self, index):
		self.lists[0].index(index)

	def insert(self, index, *elements):
		for e in elements:
			i = 0
			for l in self.lists:
				l.insert(index, e[i])
				i = i + 1

	def size(self):
		return self.lists[0].size()

	def see(self, index):
		for l in self.lists:
			l.see(index)

	def selection_anchor(self, index):
		for l in self.lists:
			l.selection_anchor(index)

	def selection_clear(self, first, last=None):
		for l in self.lists:
			l.selection_clear(first, last)

	def selection_includes(self, index):
		return self.lists[0].selection_includes(index)

	def selection_set(self, first, last=None):
		for l in self.lists:
			l.selection_set(first, last)

	def selection_get(self):
		self.lists[0].selection_get()
