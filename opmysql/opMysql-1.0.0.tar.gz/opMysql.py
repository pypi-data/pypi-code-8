#-*- coding:utf-8 -*-

import sys
import time
import os
os.environ['PYTHON_EGG_CACHE'] = '/tmp/.python-eggs'
import MySQLdb

class OP_MYSQL( object ):
	def __init__(self, host, user, passwd, port ,db,  unix_socket, charset="utf8" ):
		self.conn = None
		self.cursor = None
		self.host = host
		self.user = user
		self.passwd = passwd
		self.port = port
		self.db = db
		self.unix_socket = unix_socket
		self.charset = charset
	
	def connect(self):
		code = 0
		errMsg = ""
		try:   
			self.conn = MySQLdb.connect( host=self.host, user=self.user, passwd=self.passwd,port=self.port, db=self.db, local_infile=1, unix_socket=self.unix_socket,charset = self.charset  )
			self.cursor = self.conn.cursor() 
		except Exception, e:
			code = -1
			errMsg = str(e)		 
		return ( code, errMsg )

	def reConnect (self):
		self.close()
		return  self.connect()

	def doSql(self, tsql,reConn=1):
		code = 0
		count = 0
		errMsg = ""
		try:
			count = self.cursor.execute(tsql)
		except Exception as e:
			x,y = e.args
			if 2006==x and reConn>0 : # mysql 失去连接，重连之，然后重新执行
				code, errMsg =  self.reConnect()
				if 0 != code:
					return ( code, count, errMsg ) 
				else:
					reConn -=1 
					return self.doSql( tsql,reConn )
			else :	
				code = -1
				errMsg = str(e)
		return ( code, count, errMsg )
		
	def doSqlCreateNewTable(self,tsql,table,tableDemo, reConn=1 ):
		"""要求有建表权限"""
		code = 0
		count = 0
		errMsg = ""
		try:
			count = self.cursor.execute(tsql)    
		except Exception as e:
			x,y = e.args

			if 2006 == x and reConn>0 :
				code, errMsg =  self.reConnect() 
				if 0 != code :
					return ( code, count, errMsg )
				else:
					reConn -= 1
					return  self.doSqlCreateNewTable(tsql,table,tableDemo,reConn)
			elif 1146 == x : # table 不存在
				tsqlTable = "create table %s like %s " %( table,tableDemo)		
				try :
					count2 = self.cursor.execute( tsqlTable ) 
					code, count, errMsg = self.doSql( tsql )
				except Exception as e:
					code = -1
					errMsg = "%s:%s" %( tsqlTable,str( e ) )
			else :
				code = -1
				errMsg = str(e)
		return ( code, count, errMsg )
		
	def doSqlCreateNewDbTable(self,tsql,dbName,table,tableDemo,reConn=1):
		"""要求有建库权限"""
		code = 0
		count = 0
		errMsg = ""
		try:
			count = self.cursor.execute(tsql)    
		except Exception as e:
			x,y = e.args
			if 2006 == x and reConn>0 :  # mysql 失去连接，重连，然后 继续执行该函数
				code, errMsg =  self.reConnect()
				if 0 != code :
					return ( code, count, errMsg )
				else:
					reConn -= 1
					return self.doSqlCreateNewDbTable(tsql,dbName,table,tableDemo,reConn)
			elif 1146 == x : # table 不存在				
				tsqlTable = "create table %s.%s like %s " %(dbName,table,tableDemo)				
				try :
					count2 = self.cursor.execute( tsqlTable ) 
					code, count, errMsg = self.doSql(tsql)
				except Exception as e2:
					x2,y2 = e2.args
					if 1049 == x2 :	# database 不存在
						tsqlDb = "create database %s DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci" %( dbName )
						try :
							count3 = self.cursor.execute( tsqlDb ) 
							try :
								count4 = self.cursor.execute( tsqlTable ) 
								code, count, errMsg = self.doSql(tsql)
							except Exception as e4:
								code = -1							
								errMsg = "%s:%s" %( tsqlTable,str( e4 ) )
						except Exception as e3:
							code = -1							
							errMsg = "%s:%s" %( tsqlDb, str( e3 ) )
					else:
						code = -1
						errMsg = "%s:%s" %( tsqlTable, str( e2 ) )
			else :
				code = -1
				errMsg = str( e )
		return ( code, count, errMsg )					


	def getRet(self):
		results = self.cursor.fetchall()    
		return results
	
	def commit(self):
		self.conn.commit()
		return 0
	
	def close(self):	
		self.cursor.close()
		self.conn.close()
		return 0
		
		
	
	

