#!/usr/bin/python
import time
import datetime
import types
import urllib
import urllib2
import json

mydirs={}
values={}
class BusGpsParser(object):
	def __init__(self,db='no',cur='no'):
		self.db=db
		self.cur=cur
		self.dirs={}				
	"""It's load the source-data and the source-keys 
	   and the line_dict for get the line_id"""
	def load(self,data,keys,line_dict):	
		self.data=data		
		self.keys=keys	
		self.line_id_dict=line_dict
	"""It's call by self!"""
	def subjoin_name(self,pre):
		today=datetime.date.today()
		subfix=today.strftime("%Y%m%d");
		table_name=pre+subfix
		return table_name

	def parser(self,sp_flag):	
		temp_dirs={}
		lists=self.data.split(sp_flag)	
		for i in range(0,len(self.keys)):
			temp_dirs[self.keys[i]]=lists[i]	
		self.dirs=temp_dirs			
	"""The keys argument is very important
	   It's decide what data you want to save
	   or update to your database"""
	def recondition(self,keys):			
		self.line_no_key=self.dirs['line_no']	
		self.direction=self.dirs['direction']
		if self.dirs.has_key('gps_date'):	
			gps_time=self.datetimeTranslate('gps_date','gps_time')
			send_time=self.datetimeTranslate('send_date','send_time')
			self.dirs['gps_datetime']=gps_time
			self.dirs['send_datetime']=send_time
		elif self.dirs.has_key('stn_date'):
			stn_dt=self.datetimeTranslate('stn_date','stn_time')
			self.dirs['stn_dt']=stn_dt
		
		line_id=self.get_line_id()
		line_id=str(line_id)		
		self.dirs['line_id']=line_id
		self.keys=keys		
				
	"""It's call by self"""
	def calculator_line_id(self):
		direction=self.direction
		line_no=self.line_no_key
		if direction == '0':
			a_line_no =int (line_no)
			a_line_id=a_line_no *10 + 0 
			return str(a_line_id)
		elif direction == '1':
			b_line_no =int (line_no)
			b_line_id= b_line_no *10 + 1
			return str(b_line_id)
		else :
			print 'Error direction'

	"""It's call by self"""
	def check_dictionary(self):
		line_no_key=self.line_no_key
		line_id_dict=self.line_id_dict
		if line_id_dict.get(line_no_key) == None:
			print 'No key name as: %s' % line_no_key
		else:
			line_no=(line_id_dict.get(line_no_key))
			return str(line_no)
	"""It's call by self"""
	def get_line_id(self):
		line_no_key=self.line_no_key
		direction=self.direction
		if line_no_key.isdigit():
			line_id= self.calculator_line_id()
			return str(line_id)
		else:
			line_no=self.check_dictionary()
			self.line_no_key=line_no
			line_id= self.calculator_line_id()
			return str(line_id)
	
	def datetimeTranslate(self,arg_date,arg_time):
		_gps_datetime=self.dirs[arg_date]+' '+self.dirs[arg_time]
		_micro_second=time.mktime(time.strptime(_gps_datetime,'%Y-%m-%d %H:%M:%S'))
		_datetime="%d" % _micro_second
		return _datetime
	
	"""All for sql call ,make it fit to sql syntax"""
	def wrap(self,ruler):
		sql_data=''
		index=2
		for var in ruler:
			if isinstance(var,str):
				sql_data=str(sql_data)+','+'\''+str(self.dirs[self.keys[index]])+'\''
				index+=1
			else:
				for i in range(0,var):
					sql_data=str(sql_data)+','+str(self.dirs[self.keys[index]])
					index+=1
		return '('+sql_data[1:]+')'

	def items(self):
		sum_items=''
		for item in self.keys[2:]:
			sum_items=sum_items+','+item
		return '('+sum_items[1:]+')'
	"""just sql cmd part"""
	def equal_value(self):
		sum_items=''
		for item in self.keys[2:]:
			sum_items=sum_items+','+item+'='+'VALUES('+item+')'
		return sum_items[1:]
	"""It's for update to new table everyday!"""
	def tableName(self,arg):
		if arg == 'gps':
			gps_tn=self.subjoin_name('gps_')
			return gps_tn
		elif arg == 'stn':
			stn_tn=self.subjoin_name('stn_')
			return stn_tn
		else:
			print """Error argu: except:'stn' or 'gps' !!"""
	"""It's for your dynamic sql database table"""
	def save(self,sql_cmd):
		try:
			self.cur.execute(sql_cmd)
			self.db.commit()
		except MySQLdb.Error,e:
			print "MySQL Dynamic tables error %d:%s" % (
				e.args[0],e.args[1])
	
	"""It's for your static sql database table"""
	def update(self,sql_cmd):
		try:
			self.cur.execute(sql_cmd)
			self.db.commit()
		except MySQLdb.Error,e:
			print "MySQL Static tables erro %d:%s" % (
		e.args[0],e.args[1])
	"""It's for your check data fast and message push"""
	def post(self,url):
		values['bus_no']=self.dirs['bus_no']
		values['line_id']=self.dirs['line_id']
		values['station_no']=self.dirs['station_no']
		values['direction']=self.dirs['direction']
		values['stn_dt']=self.dirs['stn_dt']
		values['flag']=self.dirs['flag']
		try:
			jdata=json.dumps(values)
			req=urllib2.Request(url,jdata)
			response = urllib2.urlopen(req)
		except Exception,e:
			print 'Error url'
			pass
	def run_all(self):
		pass
