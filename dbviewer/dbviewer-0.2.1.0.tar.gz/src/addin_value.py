#! /usr/bin/python
# -*- coding: utf-8 -*-


import wx, sys
import sqlite3 as sqlite
import mainloader
import dbConnector
import auxiliaries
import copypaste
import config
import masterpanel


reload(sys)
sys.setdefaultencoding("utf-8")


class MainFrame(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, wx.ID_ANY, title,
									style=wx.FRAME_FLOAT_ON_PARENT|wx.DEFAULT_FRAME_STYLE)
		
		self.cp = config.confValues()
		self.db_name = self.cp.db_name
		self.table_name =self.cp.table_name
		
		self.dbc = dbcon(self.db_name)
		colname = self.dbc.col_names(self.table_name)
		colNo = len(colname)
		self.row_num = self.dbc.row_num(self.table_name)
		
		self.schema = self.dbc.check_schema(self.table_name)
		
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
		for item in colname:
			label = item
			self.tst = wx.StaticText (self.panel, id=wx.ID_ANY, label=label)
			self.layout_t.Add(self.tst, 1)
			self.layout_t.AddSpacer(10)
			
		for sch in self.schema:
			if sch == 'blob' or sch == ' ':
				self.picbtn = wx.Button (self.panel, id=wx.ID_ANY, size=(100, 30), label='choose pict')
				img = wx.EmptyImage(100, 100)
				self.ImgCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(img))
				
				self.Bind(wx.EVT_BUTTON,
						lambda event, temp=self.picbtn: self.onFileload(event, temp), self.picbtn)
				self.layout_c.Add (self.picbtn, 1)
				self.sizerP.Add (self.ImgCtrl, 1)
				
			elif sch == 'integer PRIMARY KEY':
				self.inword = wx.TextCtrl (self.panel, wx.ID_ANY, str(self.row_num +2))
				self.inword.SetFocus()
				self.layout_c.Add (self.inword, 1)
				self.keys.append(self.inword)
			else:
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
		
		self.SetSize((400, 400))
		self.panel.SetSizer(self.topsizer)
		self.Refresh()
		self.Show()
		
	def onFileload(self, event, temp):
		newsize = 100
		wid = event.GetEventObject()
		if event.Id == wid.GetId():
			fl=mainloader.Fileloader()
			data = fl.onPictloader()
			temp.SetLabel(data)
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
		
	def Cancel (self, event):
		self.dbc.commit()
		self.Destroy()
			
	def OnButton (self, event):
		dial = wx.MessageDialog(None, "Are you sure to upload", 'Question',
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
			sql = auxiliaries.insert_sql(vals, self.table_name )
			self.dbc.queries(sql, values)
			self.dbc.commit()
			

class dbcon ():
	def __init__(self, dbname):
		self.dbc = dbConnector.SqlMng(dbname)
		
	def col_names(self, tblname):
		colname = self.dbc.col_names(tblname)
		return colname
		
	def row_num (self, tblname):
		return self.dbc.row_num(tblname)
		
	def queries(self, sql, arg) :
		que = self.dbc.queries(sql, arg) 
		return que
		
	def commit (self):
		com = self.dbc.commit()
		return com 
		
	def check_schema(self, tblname):
		colname = self.col_names(tblname)
		res = []
		
		for col in colname:
			sql = "select typeof( " + col + " )"  " from " + tblname
			cur=self.dbc.query(sql)
			list = cur.fetchall()
			if len(list) == 0:
				listed = " "
			else:
				for lis in list:
					listed = [i for i in lis]
			res.append(listed)
		vals = auxiliaries.flatten(res)
		
		return vals





