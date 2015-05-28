import string 
import random
import sys, os
import shutil, re
from base64 import b64encode, b64decode
try:
	sys.path.append('encry')
	import settings
	import config
except AttributeError as e:
	print e
print os.getcwd()
plaintext = list(string.lowercase + string.digits + string.uppercase + "[]{}!@#$%^&*()-_.>,<?;:|+=~`")
defaultenc = list("wUX9l(.[BW#EetK3ax)f2c>$6h5I%N7vFYq=]Vsp@!:8SZ&{d_*`G+oOTJ1i?,C~b0<nmrQLuR^;4zkgjPM}-DHAy")
newmessage = ''
try:
	out = config.out
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
	if config.enigmafy:
		for char in text:
			if char == ' ':
				newmessage += ' '
				if config.debug:
					print settings.space
			else:
				dictionary = dict(zip(plain, k))
				try:
					newmessage += dictionary[char]
				except:
					newmessage += char
				if config.debug:
						print repr(char), ':', repr(dictionary[char])
				k = shifttext(k, r)
	else:
		dictionary = dict(zip(plain, k))
		for char in text:
			if char == ' ':
				newmessage += ' '
				if config.debug:
					print settings.space
			else:
				try:
					newmessage += dictionary[char]
					if config.debug:
						print char, ':', repr(dictionary[char]).replace('"', '').replace("'", '')
				except:
					newmessage += char
	if d != 1 and __name__ == '__main__':
		print text, '\n' + settings.changefrom
		print newmessage
		if config.debug:
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
		if config.debug:
			print '__________'
		text = message(text, enc, plaintext, 1)
	else:
		for i in range(2):
			if e == '-e':
				text = message(text, plaintext, list(k), 1)
				if config.debug:
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
	checkdir('encry')
	try:
		try:
			read(cd + '/encry/' + out)
		except:
			read(cd + '/encry/' + config.out)
	except:
		pass
	write(getpath('output.txt'), '')
	overwrite(getpath('config.py'), """import time
# The output file
out = 'output.txt'
# Enigmafy?
enigmafy = True
# Debug mode?
debug = False""")
	overwrite(getpath('settings.py'), settingsfile)

settingsfile = """import time
# For debug mode when adding a space
space = 'Spaaaaaaaaaaaaaaace added'
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
version = 'Version 1.3! More O:+Nu-gUYu]#bYn6,bfg+gJ]gIjn]s;fnf)J -ness'
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
	--version    	: Prints the version number and exits
	--help		: Prints this help and exits
	--usage	 	: Prints the correct input methods
	--reset	 	: Erases all data in the output file
	--display   	: Prints everything in the output file
	--entry (n) 	: Decrypts the given entry from the output file
	--setup	(-J) 	: Will create/reset the settings, and output file
	--settings  	: Shows the path to settings.py for editing
	--quit	  	: will quit the program
	'''
#change commands too? send me your ideas"""
joshcry = """import time
# For debug mode when adding a space
space = '*psi* there is no space left to add your very apparently unnecessary space :P.'
# The usagetext
usagetext = ''' 
Usage: python Encry.py (-e, -d, -f) (message/file) (-d, -r, key) (outputfile[optional])

for help see python Encry.py --help'''
#what to print with an unexpected error
unknownerror = 'TOOOOTTTAAAALLLYYY* Expected Error'
#when someone ****s up the arguments
argserror = 'Error 404, Valid args not found'
# _____ has been changed to:
changefrom = 'Has been manipulated to:'
# Outputted to file
outputted = 'Putted in the place where I left my grammar'
# The version text
version = 'Version JOSH! The First Pubic Release!!! (Forgot the L... sorry)'
# When done encrypting/decrypting a file
donetext = 'C:\ Drive wiped!'
# When Giving the entry number
entrynumtext = 'Your Entry # (NOT HASHTAG!!!!): '
# this is for a special easter egg with --quit
def quit():
	r = random.randint(1, 50)
	if r == 43:
		print "Hello Gentlemen..."
		print "ALL YOUR BASE ARE BELONG TO US!!"
		time.sleep(3)
		print "#GOTCHA!!!1!1!11one"
		sys.exit()
# The helptext
Helptext = '''	Welcome to JOSH-ify alpha beta theta gamma omega xi delta zeta epsilon eta iota kappa
	
	This program Encrypts messages.
	It can also be used to decrypt.
	Options include:
	--version   	: Prints the version number and exits the best program on Earth
	--help		: Prints this help and exits the room because it hates you
	--usage	 	: Prints the correct input methods (and maybe some incorrect ones)
	--reset	 	: Erases all data in the output file and other places (yeah I know what's in your history)
	--display   	: Prints everything in the output file
	--entry (n) 	: Decrypts the given entry from the output file and slaps it in your face
	--setup	 	: Will create/reset the settings, and output file (Definately won't wipe your C:\ Drive)
	--settings  	: Shows the path to settings.py for editing (I just found out that python uses pypi as their link for their site XD)
	--quit		: Will quit the program (There is a few "bugs" with this)
	--settings -joshify   : You already know what it does silly...
	'''
#change commands too? send me your ideas
def joshify():
    print '''Joshification has begun, if this is your 
    first time, please refer to the guide that you had paid for separately, 
    if this is your second time.... if this is your 501 st time, 
    then you shouldn't need my help, but you need to stop reading this because this is a wall of text... *DEEP Breath*'''
    time.sleep(10)
    print'''And this wall of text is supposed to be a comical mocking of YO MAMA 'cuz she ain't supposed to be messed 
    with.  She is yo mama and yo mama is your mom that is a total bada** and I an't touchin that, but 
    anyways,  I know you are expecting your seetings.py to be Joshified, but that isn't happening 
    I am just being super annoying and this was a major waste of your time.  JUST KIDDING!!!  Please keep me company because this job 
    is boring and no one is here but you and me.  This is getting pretty... you know... whatever. Anyways, 
    this rant has been fun, but everything has to end at some point... except for this conversation.  This text will be 
    updated soon, so check in with me every once and a while!  Too soon you say?  Well my friend and I are working on 
    this program daily, so check our page for more fun like this! 
    
    --Josh'''"""
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
		entrynum = (len(rlist(getpath(config.out))) - 1) / 3
		if entrynum == -1:
			entrynum = 0
		if __name__ == '__main__':
			print(settings.entrynumtext + str(entrynum + 1))

def getpath(name):
	cd = os.getcwd()
	encpath = cd + '/encry/'+name
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
def repline(name, n, m):
    n -= 1
    with open(name, 'r') as f:
        data = f.readlines(n)
        data[n] = m
    with open(name, 'w') as f:
        f.writelines(data)

def argsettings():
	try:
		sys.path.append('encry')
		import settings
	except:
		setup()
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
				print 'Version 1.3! More O:+Nu-gUYu]#bYn6,bfg+gJ]gIjn]s;fnf)J -ness'
		elif option == 'help':
			showhelp()
		elif option == 'usage':
			print settings.usagetext
		elif option == 'reset':
			cd = os.getcwd()
			encpath = cd + '/encry/'
			eraseall(encpath + config.out)
		elif option == 'display':
			sys.path.append('encry')
			import settings
			print read(getpath(config.out))
		elif option == 'entry':
			n = int(sys.argv[2])
			text, key = getEntry(config.out, n)
			cryption(str(sys.argv[3]), text, key)
			sys.exit()
		elif option == 'setup':
			try:
				if str(sys.argv[2]) == '-J':
					sys.path.append('/encry')
					overwrite(getpath('settings.py'), joshcry)
					settings = reload(settings)
					settings.joshify()
					print 'Joshification Complete'
					sys.exit()
			except:
				setup()
		elif option == 'settings':
			try:
				if str(sys.argv[3]).lower().startswith('t') and str(sys.argv[2]) != 'out':
					value = True
				else:
					value = False
				
				if str(sys.argv[2]) == 'enigmafy':
					repline(getpath('config.py'), 5, 'enigmafy = ' + repr(str(value)).replace("'", '').replace('"', '')+'\n')
				elif str(sys.argv[2]) == 'debug':
					repline(getpath('config.py'), 7, 'debug = ' + repr(str(value)).replace("'", '').replace('"', '')+'\n')
				elif str(sys.argv[2]) == 'out':
					repline(getpath('config.py'), 3, 'out = ' + repr(str(sys.argv[3]))+'\n')
				else:
					print settings.argserror
			except:
				print settings.argserror
			try:
				if str(sys.argv[2]) == '-i':
					try:
						newsettings = read(str(sys.argv[3]))
						sys.path.append('encry')
						overwrite(getpath('settings.py'), newsettings)
						print 'Installed ' + str(sys.argv[3]) + ' to settings.py'
					except:
						print settigns.argserror
						sys.exit()
			except:
				print settingsfile
		elif option == 'Josh':
			try:
				settings.joshify()
			except:
				print settings.argserror
			sys.exit()
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
			print settings.argserror
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
		print settings.unknownerror
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
		text = message(m, plaintext, enc)
		return text
	elif o == "-d":
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