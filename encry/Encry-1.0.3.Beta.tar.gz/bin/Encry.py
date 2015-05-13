import string 
import random
import sys, os
import shutil, re
from base64 import b64encode, b64decode
try:
	sys.path.append('encry')
	import settings
except AttributeError as e:
	print e

plaintext = list(string.lowercase + string.digits + string.uppercase + "[]{}!@#$%^&*()-_.>,<?;:|+=~`")
defaultenc = list("wUX9l(.[BW#EetK3ax)f2c>$6h5I%N7vFYq=]Vsp@!:8SZ&{d_*`G+oOTJ1i?,C~b0<nmrQLuR^;4zkgjPM}-DHAy")
newmessage = ''
try:
	out = settings.out
except:
	out = 'output.txt'
enc = defaultenc
k = ''
d = 0
l = 0

def message(text, plain, k, d = 0):
	newmessage = ''
	if ''.join(plain).startswith(string.lowercase):
		key = k
		r = 'k1'
	else:
		key = plain
		r = 'k2'
	ok = ''.join(key)
	if settings.enigmafy:
		for char in text:
			if char == ' ':
				newmessage += ' '
				if settings.debug:
					print settings.space
			else:
				dictionary = dict(zip(plain, k))
				try:
					newmessage += dictionary[char]
					if settings.debug:
						print repr(char), ':', repr(dictionary[char])
				except:
					newmessage += char
				k = shifttext(k, r)
	else:
		dictionary = dict(zip(plain, k))
		for char in text:
			if char == ' ':
				newmessage += ' '
				if settings.debug:
					print settings.space
			else:
				try:
					newmessage += dictionary[char]
					print char, ':', repr(dictionary[char]).replace('"', '').replace("'", '')
				except:
					newmessage += char
	if d != 1 and __name__ == '__main__':
		print text, '\n' + settings.changefrom
		print newmessage
		if settings.debug:
			print 'Key Used:\n' + ''.join(key)
		to_File(newmessage, ''.join(key))
		print settings.outputted
	elif d == 1:
		return newmessage
	else:
		return newmessage, key

def doublecrypt(text, k, e, p = True):
	oldtext = text
	if e == '-d':
		text = message(m, enc, plaintext, 1)
		if settings.debug:
			print '__________'
		text = message(text, enc, plaintext, 1)
	else:
		for i in range(2):
			if e == '-e':
				text = message(text, plaintext, list(k), 1)
				if settings.debug:
					print '__________'
	if __name__ == '__main__' and p != False:
		print oldtext, '\n' + settings.changefrom
		print text
		if str(k) == str(plaintext):
			k = ''.join(k)
		else:
			pass
		to_File(text, ''.join(k))
		print settings.outputted
	else:
		return text

def to_File(n, k):
	try:
		cd = os.getcwd()
		encpath = cd + '/encry/' + out
		newEntry(encpath, k, n)
	except IOError as e:
		print settings.unknownerror, sys.exc_info()[0]
		raise	

def setup():
	cd = os.getcwd()
	encpath = cd + '/encry'
	checkdir('encry')
	try:
		try:
			read(cd + '/encry/' + out)
		except:
			read(cd + '/encry/' + settings.out)
	except:
		pass
	write(encpath + '/output.txt', '')
	overwrite(encpath + '/settings.py', """
# The output file
out = 'output.txt'
# Enigmafy?
enigmafy = True
# Debug mode?
debug = False
# For debug mode when adding a space
space = 'Spaaaaaaaaaaaaaaace'
# The usagetext
usagetext = ''' 
Usage: python Encry.py (-e, -d, -f) (message/file) (-d, -r, key) (outputfile[optional])

for help see python Encry.py --help'''
#what to print with an unexpected error
unknownerror = 'Unexpected Error'
#when someone ****s up the arguments
argserror = 'Error, Invalid args'
# _____ has been changed to:
changefrom = 'Has been Changed to:'
# Outputted to file
outputted = 'Outputted to file'
# The version text
version = 'Version 2.5! The Userbility Update!'
# When done encrypting/decrypting a file
donetext = 'Done!'
# When Giving the entry number
entrynumtext = 'Your Entry Number: '
# this is for a special easter egg with --quit
def quit():
	r = random.randint(1, 50)
	if r == 43:
		print "Don't be a quitter!"
		print "I'm not letting you quit"
		time.sleep(1)
		print "jk just do --quit again"
		sys.exit()
# The helptext
Helptext = '''	Welcome to Encry.py
	
	This program Encrypts messages.
	It can also be used to decrypt.
	Options include:
	--version   : Prints the version number and exits
	--help		: Prints this help and exits
	--usage	 	: Prints the correct input methods
	--reset	 	: Erases all data in the output file
	--display   : Prints everything in the output file
	--entry (n) : Decrypts the given entry from the output file
	--setup	 	: Will create/reset the settings, and output file
	--quit		: will quit the program
	'''
#change commands too? send me your ideas""")

def shifttext(text, shift):
	text = list(text)
	if shift == 'k1':
		x = text.pop(0)
		text.append(x)
		return text
	elif shift == 'k2':
		x = text.pop()
		text.insert(0, x)
		return text

class encry():
	def __init__(self, message, k):
		self.message = message
		self.k = k
	def encrypt(self):
		if str(self.k) == '-r':
			k = randKey(plaintext)
		elif str(self.k) == '-d' or str(self.k) == 'Default':
			k = defaultenc
		else:
			k = str(self.k)
		newmessage = message(str(message), plaintext, list(k))
		if self.k == '-d':
			k = 'Default'
		else:
			k = ''.join(self.k)
		return newmessage, k
	def decrypt(self): 
		if str(self.k) == '-d':
			k = defaultenc
		else:  
			k = str(self.k)
		newmessage = message(str(message), list(k), plaintext)
		if self.k == '-d':
			k = 'Default'
		else:
			k = ''.join(self.k)
		return newmessage, k
	
def randKey():
	new = list(plaintext)
	plain = random.shuffle(new)
	return ''.join(new)

def getEntry(name, entry):
	cd = os.getcwd()
	name = cd + '/encry/' + name
	entry = int(entry) * 3
	text = repr(singleline(name, entry)).replace("'", '').replace('"', '')
	entry += 1 
	key = repr(singleline(name, entry)).replace("'", '').replace('"', '')
	return text, key

def newEntry(name, k, m):
	with open(name, 'a') as f:
		f.write('\n\n')
		f.write(repr(m).replace("'", '').replace('"', ''))
		f.write('\n')
		f.write(repr(''.join(k)).replace("'", '').replace('"', ''))
		entrynum = (len(rlist(getpath(settings.out))) - 1) / 3
		if entrynum == -1:
			entrynum = 0
		if __name__ == '__main__':
			print(settings.entrynumtext + str(entrynum + 1))

def getpath(name):
	cd = os.getcwd()
	encpath = cd + '/encry/' + name
	return encpath

#from file.py
def write(name, m):
	with open(name, 'a') as f:
		f.write(str(m))
def read(name, n = 1):
	with open(name, 'r') as f:
		lines = f.readlines(n)
		lines = ''.join(lines)
		return lines
def eraseall(name):
	with open(name, 'w') as f:
		f.write('')
def singleline(name, n):
	n = int(n) - 1
	with open(name, 'r') as f:
		lineList = f.readlines()
		return lineList[n].replace('\n', '')
def encode(file):
	m = read(file)
	m = ''.join(m)
	m = b64encode(m)
	overwrite(file, m)
def overwrite(name, m):
	with open(name, 'w') as f:
		f.write(m)
def decode(file):
	m = read(file)
	m = ''.join(m)
	m = b64decode(m)
	overwrite(file, m)
def overwrite(name, m):
	with open(name, 'w') as f:
		f.write(m)
def checkdir(path):
	try:
		os.makedirs(path)
	except OSError:
		if not os.path.isdir(path):
			raise
def rlist(name):
	with open(name, 'r') as f:
		lines = f.readlines(1)
		return lines
def findrepl(name, torep, repwith):
    lines = open( name, "r" ).readlines()
    newlines = []
    for line in lines:
        line = re.sub( torep, repwith, line )
        newlines.append(line)
    newlines = ''.join(newlines)
    overwrite(name, newlines)

def argsettings():
	try: 
		o = str(sys.argv[1])
	except:
		print settings.argserror
		sys.exit()
	if str(sys.argv[1]) == '-h':
		showhelp()
	if str(sys.argv[1]).startswith('--'):
		option = sys.argv[1][2:]
		# Fetch sys.argv[1] and copy the string except for first two characters
		if option == 'version':
			try:
				print settings.version
			except:
				print 'Version 2.5! The userbility Update!'
		elif option == 'help':
			showhelp()
		elif option == 'usage':
			print settings.usagetext
		elif option == 'reset':
			cd = os.getcwd()
			encpath = cd + '/encry/'
			eraseall(encpath + settings.out)
		elif option == 'display':
			print read(getpath(settings.out))
		elif option == 'entry':
			n = int(sys.argv[2])
			text, key = getEntry(settings.out, n)
			cryption(str(sys.argv[3]), text, key)
			sys.exit()
		elif option == 'setup':
			setup()
		elif option == 'settings':
			findrepl(getpath('settings.py'), str(sys.argv[2]), str(sys.argv[3]))
		elif option == 'quit':
			try:
				settings.quit()
			except:
				r = random.randint(1, 50)
				if r == 43:
					print "Don't be a quitter!"
					print "I'm not letting you quit"
					time.sleep(1)
					print "jk just do --quit again"
			sys.exit()
		else:
			print settings.unexpectederror
		sys.exit()
	if sys.argv[1] == '-f':
		f = str(sys.argv[2])
		e = str(sys.argv[3])
		if e == '-e':
			encode(f)
		elif e == '-d':
			decode(f)
		print settings.donetext
		sys.exit()
	if len(sys.argv) >5:
		print settings.unexpectederror
		sys.exit()
	o = str(sys.argv[1])
	m = str(sys.argv[2])
	k = str(sys.argv[3])
	try:
		out = str(sys.argv[4])
	except:
		pass
	if str(k) == '-d':
		enc = defaultenc
	elif str(k) == '-r':
		enc = randKey()
	else:
		k = str(k)
		enc = list(k)
	cryption(o, m, enc)
def cryption(o, m, enc):
	if o == "-e":
		print m
		text = message(m, plaintext, enc)
		return text
	elif o == "-d":
		print m
		text = message(m, enc, plaintext)
		return text
	elif o == "-ee":
		text = doublecrypt(m, enc, '-e')
		return text
	elif o == "-ed":
		text = doublecrypt(m, enc, '-d')
		return text
def showhelp():
	print settings.Helptext

if __name__ == '__main__':
	argsettings()