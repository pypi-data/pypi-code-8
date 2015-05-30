#!/usr/bin/python
#coding:utf-8
#--------------------------------
#Author:	Frank AK			-
#Org   :	Landpack			-
#Email :	landpack@sina.com	-
#--------------------------------

class akParser:
	def __init__(self,your_data,your_key,your_key_list_len):
	
		self._data=your_data
		self._key=your_key
		self._key_list_len=your_key_list_len
		self._dict={}
	
	def parser(self,delimiter='|',head_retain=True,tail_retain=True):
		"""This function expect 3 argument,for parser your data"""
		_tmp_list=self._data.split(delimiter)
		if head_retain and tail_retain:
			pass
		elif head_retain and not tail_retain:
			_tmp_list=_tmp_list[:-1]
		elif not head_retain and tail_retain:
			_tmp_list=_tmp_list[1:]
		elif not head_retain and not tail_retain:
			_tmp_list=_tmp_list[1:-1]


		if len(self._key) == self._key_list_len:
			for i in range(0,self._key_list_len):
				self._dict[self._key[i]]=_tmp_list[i]
		else:
			print "The key your give which dones't match lenght"
			pass
		return self._dict
	
	def transType(self,ruler):
		index_key=0
		for var in ruler:
			if isinstance(var,str):
				index_key+=1
			else:
				for i in range(var):
					self._dict[self._key[index_key]]=int(self._dict[self._key[index_key]])
					index_key+=1
		return self._dict

if __name__ == '__main__':

	string='|201221811062|23|60|5008|'
	keys=['id','age','weight','phone']
	length=4

	obj = akParser(string,keys,length)
	mydict=obj.parser('|',False,False)
	print 'mydict',mydict 
	ruler=['s',1,2]
	newdict=obj.transType(ruler)
	print 'newdict',newdict



	sample = """*|GPS|1729|K2|2006-01-04|13:15:08|6000.0000|2000.0000\
|40|140|4|5|1|2006-01-04|13:01:04|0|0|0|01000932|1|#*"""
	mykeys=['star','cmd','bus_no','line_no','gps_date',
			'gps_time','latitude','longitude','speed+','angle',
			'next_station','people_num','start_end_flag','send_date','send_time',
			'direction','run_status','leave_flag','driver_no','driver_flag',
			'endstart']

	obj2=akParser(sample,mykeys,21)
	mydict2=obj2.parser('|',True)
	print mydict2
