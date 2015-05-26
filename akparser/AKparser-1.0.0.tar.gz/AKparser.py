#!/usr/bin/python
#coding:utf-8
#--------------------------------
#Author:	Frank AK			-
#Org   :	Landpack			-
#Email :	landpack@sina.com	-
#--------------------------------
class akparser:
	def __init__(self,string,keys,length):
		"""It's init data,and keys,number of item"""
		self.string=string
		self.keys=keys
		self.length=length
		self.temp_dict={}

	def akparser(self,sp_flag,head=True,tail=True):
		"""It's split by the sp_flag"""
		lists=self.string.split(sp_flag)
		print 'len==',len(lists)
		if head == True and tail == True:
			lists=lists
		elif head == True and tail == False:
			lists=lists[:-1]
		elif head == False and tail == True:
			lists=lists[1:]
		elif head == False and tail == False:
			lists=lists[1:]
			lists=lists[:-1]

		if len(self.keys) == self.length:
			for i in range(0,len(self.keys)):
				self.temp_dict[self.keys[i]]=lists[i]
		else:
			print "The keys your get whict doesn't match length"
			pass
		return self.temp_dict

if __name__ == '__main__':
	string='|201221811062|23|60|5008|'
	keys=['id','age','weight','phone']
	length=4

	obj = akparser(string,keys,length)
	mydict=obj.akparser('|',False,False)
	print mydict



	sample = """*|GPS|1729|K2|2006-01-04|13:15:08|6000.0000|2000.0000\
|40|140|4|5|1|2006-01-04|13:01:04|0|0|0|01000932|1|#*"""
	mykeys=['star','cmd','bus_no','line_no','gps_date',
			'gps_time','latitude','longitude','speed+','angle',
			'next_station','people_num','start_end_flag','send_date','send_time',
			'direction','run_status','leave_flag','driver_no','driver_flag',
			'endstart']

	obj2=akparser(sample,mykeys,21)
	mydict2=obj2.akparser('|',True)
	print mydict2

