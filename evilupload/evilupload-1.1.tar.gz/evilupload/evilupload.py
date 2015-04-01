from io import open

import requests, mechanize, cookielib
import sys, os
import re
from getpass import getpass

try:
	# Python 2
        prompt = raw_input
except NameError:
        # Python 3
        prompt = input
COOKIEFILE = (os.environ['HOME'] + '/.EZuploader/cookies.lwp') #TODO: implement cookies local storage, see if it works

def get_file_size(filename):
	if os.path.exists(filename):
		size = os.stat(filename).st_size
		if size <= 0:
			raise ValueError('File size too small.')
		if size > 1*1024*1024*1024:
			raise ValueError('File is larger than 1GB.')
	else:
		raise OSError('No such file or directory: %s' %filename)	

def get_image_size(filename):
	if os.path.exists(filename):
		size = os.stat(filename).st_size
		if size <= 0:
			raise ValueError('File size too small.')
		if size > 30*1024*1024:
			raise ValueError('File is larger than 1GB.')
	else:
		raise OSError('No such file or directory: %s' %filename)	 

def read_file(infilename):#TODO: read files in chunks than load it all in memory
	try:
       		infile = open(infilename, 'rb')
       		content = infile.read()
       		infile.close()
       		return content
	except IOError as err:
		raise "Error reading file: %s"%err

def is_supported_image(image):
	supported_ext = ['gif', 'jpeg', 'png', 'bmp']
	image_ext = os.path.splitext(image)[1]
	if image_ext[1:] in supported_ext:
		return True
	else:
		return False

def get_link(html):
	r_ul = re.compile(r'\s*(?i)href\s*=\s*(\"([^"]*\")|"[^"]*"|([^"">\s]+))')
	link = re.findall(r_ul, html)
	return link[0][0]

class EZuploader():
	def __init__(self, filename=None):
		self.filename = filename
		self.forum = 'https://evilzone.org/index.php'#
		self.host = 'upload.evilzone.org'
		self.url = 'http://{0}'.format(self.host)
		self.cj = None #load_cookies()
		
		self.agent = 'Mozilla/5.0 (X11; Linux i686; rv:25.0) Gecko/20100101 Firefox/25.0'
		self.type = 'multipart/form-data'
		self.referer = 'http://upload.evilzone.org/index.php?page=fileupload'
		self.headers = {'content-type': self.type, 'User-Agent': self.agent, 'Referer': self.referer}
	
	

	def login(self):
		if self.cj is None:
			login_url = 'https://evilzone.org/login'
			username = prompt('Username for Evilzone.org: ')
			password = getpass('Password for Evilzone.org: ')
			#print username, password

			agent = mechanize.Browser()
			agent.set_handle_robots(False)
			self.cj = cookielib.LWPCookieJar()
			
			agent.set_cookiejar(self.cj)
			agent.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
			agent.open(login_url)
	
			#login
			agent.select_form(name='frmLogin')
			agent.form['user'] = username
			agent.form['passwrd'] = password
			response = agent.submit()
	
			if response.code == requests.codes.ok:
				#print response.code
				self.cj.save
				#print self.cj
				return None
		
	def fileupload(self, filename=None):
		path = '/index.php?page=fileupload&filename={0}'
		filepath = filename or self.filename
		_filename = os.path.basename(filepath)
		file_url = self.url + path.format(_filename)
		size = get_file_size(filepath)
		self.headers['Content-Length'] = size
		
		if self.cj is not None:
			session = requests.session()
			#r = session.get(url='https://evilzone.org/rauploadmod.php',
			#		 headers=self.headers, data=read_file(filepath), cookies=self.cj)
			r = session.post(url=file_url, headers=self.headers, data=read_file(filepath), cookies=self.cj)
			
		else:
			print 'Posting anonymously'
			r = requests.post(url=file_url, headers=self.headers, data=read_file(filepath))
		if 'Error' not in r.text:
			return 'http://upload.evilzone.org?page=download&file='+r.text
		else:
			return None

	def imageupload(self, filename=None):
		path = '/index.php?page=imageupload&upload=true'
		imagepath = filename or self.filename
		image_url = self.url + path
		size = get_image_size(imagepath)
		self.headers['Content-Length'] = size
		if is_supported_image(imagepath):
			if self.cj is not None:
				#print self.cj
				r = requests.post(url=image_url, headers=self.headers, data=read_file(imagepath), cookies=self.cj)
			else:
				r = requests.post(url=image_url, headers=self.headers, data=read_file(imagepath))
			if 'Error' not in r.text:
				return self.url + '/' + get_link(r.text).strip('"')
			else:
				return None
		else:
			raise TypeError("Image format not supported.")

#	def delete():
#		delete= 'http://upload.evilzone.org/index.php?page=yourimages&delete=S7YDymME33ZidFLEagaQ6YfC7KMCDEUREFMg7piNjlGHXpOFrz'
#		delete='http://upload.evilzone.org/index.php?page=yourfiles&delete=8wPtrctGEoETO7lIbX38Y3QqyAYXQMqchWxUpBSYLND5FT9RO1'
