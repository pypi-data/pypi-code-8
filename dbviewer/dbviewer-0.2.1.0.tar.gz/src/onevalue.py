#! /usr/bin/python
# -*- coding: utf-8 -*-


import wx, sys, os
import sqlite3 as sqlite
import mainloader
import savedialog
import dbConnector
import auxiliaries
import copypaste
import config
import masterpanel
import tablemaker


reload(sys)
sys.setdefaultencoding("utf-8")


class MainFrame(wx.Frame):
	def __init__(self, parent, arg, argv, column=None, types=None):
		wx.Frame.__init__(self, parent, wx.ID_ANY,
									style=wx.FRAME_FLOAT_ON_PARENT|wx.DEFAULT_FRAME_STYLE)
		
		self.db_name = arg
		self.table_name =argv
		self.colname = column
		self.colNo = len(self.colname)
		self.schema = types
		
		#self.dbc = dbConnector.SqlMng(self.db_name)
		
		# ------------------ Panel & Sizer --------------------------------------------------
		
		self.panel = masterpanel.MasterPanel (self)
		self.topsizer = wx.BoxSizer (wx.VERTICAL)
		self.layout_t = wx.BoxSizer(wx.HORIZONTAL)
		self.layout_p = wx.BoxSizer(wx.HORIZONTAL)
		self.layout_c = wx.BoxSizer(wx.HORIZONTAL)
		self.sizerP = wx.BoxSizer(wx.HORIZONTAL)
		self.layz = wx.BoxSizer(wx.HORIZONTAL)
		
		# ------------------------ Text ------------------------------------------------------
		
		self.keys = []
		for item in self.colname:
			label = item
			self.tst = wx.StaticText (self.panel, id=wx.ID_ANY, label=label)
			self.layout_t.Add(self.tst, 1)
			self.layout_t.AddSpacer(10)
			
		for sch in self.schema:
			if sch == 'blob' or sch == ' ':
				self.picbtn = wx.Button (self.panel, id=wx.ID_ANY, size=(100, 30), label='choose pict')
				img = wx.EmptyImage(100, 100)
				self.ImgCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(img))
				
				self.Bind(wx.EVT_BUTTON, self.onFileload, self.picbtn)
				self.layout_c.Add (self.picbtn, 1)
				self.sizerP.Add (self.ImgCtrl, 1)
				
			else :
				self.word = wx.TextCtrl (self.panel, wx.ID_ANY)
				self.word.SetFocus()
				self.layout_c.Add (self.word, 1)
				self.keys.append(self.word)
				
		# ------------ MenuBar --------------------------------------------------------------
				self.menu = copypaste.Copypaste(self.word)
				self.SetMenuBar(self.menu)
				self.Bind(wx.EVT_MENU, self.menu.onCut, id=106)
				self.Bind(wx.EVT_MENU, self.menu.onCopy, id=107)
				self.Bind(wx.EVT_MENU, self.menu.onPaste, id=108)
				self.Bind(wx.EVT_MENU, self.menu.onDelete, id=109)
				self.Bind(wx.EVT_MENU, self.menu.onSelectAll, id=110)
		
		# ------------ Button -------------------------------------------------------------------
		
		cancel = wx.Button(self.panel, wx.ID_ANY, 'Close')
		btn = wx.Button (self.panel, wx.ID_ANY, 'Insert Data')
		cancel.Bind(wx.EVT_BUTTON, self.Cancel)
		btn.Bind(wx.EVT_BUTTON, self.OnButton)
		self.layz.Add(cancel)
		self.layz.Add(btn)
		
		# --------------- Add in Topsizer ------------------------------------------------------
		
		self.topsizer.Add (self.layout_t, 0, wx.EXPAND | wx.ALL, 10)
		self.topsizer.Add (self.layout_c, 0, wx.EXPAND | wx.ALL, 5)
		self.topsizer.Add (self.layout_p, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
		self.topsizer.Add (self.sizerP, 0, wx.GROW | wx.ALL, 5)
		self.topsizer.Add (self.layz, 0, wx.TOP | wx.RIGHT | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM, 10)
		
		self.SetSize((500, 400))
		self.panel.SetSizer(self.topsizer)
		self.Refresh()
		self.Show()
		
	def onFileload(self, event):
		fl=mainloader.Fileloader()
		data = fl.onPictloader()
		newsize = 100
		self.picbtn.SetLabel(data)
		if event.Id == self.picbtn.Id:
			self.keys.append(sqlite.Binary( data ))
			
		with open ( data, 'rb') as input_file:
			image = wx.Image(data)
		self.resize(image, newsize)
		self.ImgCtrl.SetBitmap(wx.BitmapFromImage(image))
	
	def resize (self, image, newsize):
		orgWidth = image.GetWidth()
		orgHeight = image.GetHeight()
		if orgHeight < orgWidth :
			targWidth = newsize
			targHeight = orgHeight * targWidth / orgWidth
			
		elif orgWidth <= orgHeight:
			targHeight = newsize
			targWidth = orgWidth * targHeight/ orgHeight
		return image.Rescale(targWidth, targHeight)
		
	def createTable(self):
		lst=[]
		for i in range( self.colNo ):
			lst.append(self.colname[i] + ' ' + self.schema[i])
		sql = ("create table " + self.table_name + "(" + ', '.join(['%s']*len(lst)) + ")") % tuple(lst)
		print sql
		
		return sql
			
	def OnButton (self, event):
		dial = wx.MessageDialog(None, "Are you sure to make new file?", 'Question',
													wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		ret = dial.ShowModal()
		if (ret == wx.ID_YES) :
			vals =[]
			keyword = self.keys
			for kw in keyword:
				if isinstance(kw, wx._controls.TextCtrl) :
					vals.append(kw.GetValue())
				else:
					vals.append(kw)
			values = tuple(vals)
			
			if not os.path.exists(self.db_name):
				savedialog.saveDialog(self.db_name)
			self.dbc = dbConnector.SqlMng(self.db_name)
			self.dbc.query(self.createTable())
			ins_sql = auxiliaries.insert_sql(vals, self.table_name )
			print ins_sql
			self.dbc.queries(ins_sql, values)
			self.dbc.commit()
			self.Destroy()
			
	def Cancel (self, event):
		self.dbc.commit()
		self.Destroy()
			




