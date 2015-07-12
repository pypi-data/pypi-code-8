import requests
from bs4 import BeautifulSoup
import operator
from collections import OrderedDict


#Crawls out a link and should return post count
url = raw_input("Enter URL in correct format: ")

#url = "https://forum.sorbmc.com/index.php?topic=12728"
#to test : https://forum.sorbmc.com/index.php?topic=2340.msg131810;topicseen#new
flag1 = 0
flag3 = 0 #flags for testing of exceptions
temp = ''
try:
	temp = url.split('=',1)[1]
except:
	flag1 = 1
try:
	num_th = temp.split('.',1)[0]
except :
	num_th = temp

try:
	r = requests.get(url)
except:
	flag3 = 1

#print flag3 , flag1

if flag3 ==0 and flag1 == 0:
	url = "https://forum.sorbmc.com/index.php?topic="+num_th
	#print url
	r = requests.get(url)
	if r.status_code == 200:
		data = BeautifulSoup(r.text, 'html.parser')



		users =[]
		d ={}
		cnt = 1

		
		filt_count = data.find_all("a", { "class" : "navPages"})
		
		for n in filt_count:
			#print a.text
			if n.text > cnt:
				cnt = n.text
				#print cnt

		print 'Total Pages :',cnt
		print '---------------------------------------------------------------------'
		print ' Scraping through data, please be patient, it can take a bit of time'
		print '---------------------------------------------------------------------'
		#print filt
		term =0
		count = int(cnt)
		for i in range(0,count):
			term = 15*i
			url2 = url +"." + str(term)
			#print url2
			#print term
			
			r2 = requests.get(url2)	
			data2 = BeautifulSoup(r2.text, 'html.parser')
			filt = data2.find_all("h4", { "class" : "perfiltitle" })


			for f in filt:
				#print f.a.text
				try:
					if f.a.text in d:
						d[f.a.text]+=1
					else:
						d[f.a.text]=1

				except:
					if f.text in d:
						st = str(f.text)
						st = st.strip()
						d[st]+=1
					else:
						st = str(f.text)
						st = st.strip()
						d[st]=1
		#newA = dict(sorted(d.iteritems(), key=operator.itemgetter(1), reverse=True)[:5])
		d_d = OrderedDict(sorted(d.items(), key=lambda kv: kv[1], reverse=True)[:10])

		#print len(d_d)
		if len(d_d) != 0:
			print ' TOP 10 POSTERS : <name> <post_count>'
			print "---------------------------------------"
			for key in d_d:
				print key, d_d[key]
	else:
		print 'ERROR : Please make sure the link you provided is correct and matching the sorb forum thread format'
	#print sorted_x.reverse()
else:
	print 'ERROR : Please make sure the link you provided is correct and matching the sorb forum thread format'
	
#print r.text