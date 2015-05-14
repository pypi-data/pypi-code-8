#!/usr/bin/python
import sys, binascii, shutil, os, re
from path import path
class text():
	def __init__(self, text):
		self.text = text
	def literal(self):
		return repr(self.text)
	def caps(self, mode):
		if mode == 'switch':
			return self.text.switchcase()
		if mode == 'title':
			return self.text.title()
		if mode == 'fix':
			return self.text.capitalize()
	def rev(self):
		return ''.join(reversed(self.text))
def write(name, m):
    with open(name, 'a') as f:
        f.write(m)
def read(name, n = 1):
    with open(name, 'r') as f:
        lines = f.readlines(n)
        lines = ''.join(lines) 
        return lines
def overwrite(name, m):
    with open(name, 'w') as f:
        f.write(m)
def eraseall(name):
    with open(name, 'w') as f:
        f.write('')
def newline(name):
    with open(name, 'a') as f:
        f.write("\n")
def singleline(name, n):
    n = int(n) - 1
    with open(name, 'r') as f:
        lineList = f.readlines()
        return lineList[n].replace('\n', '')
def copy(name, file):
    with open(name, 'r') as f:
        tocopy = read(name)
    with open(file, 'w') as f:
        f.write(tocopy)
def strline(name, n):
    n = int(n) - 1
    with open(name, 'r') as f:
        lineList = f.readlines()
        line = lineList[n].replace("\n", "")
        return line
def charcount(name):
    with open(name, 'r') as f:
        lines = f.read()
        lines = ''.join(lines).replace("\n", "")
        return len(lines)
def linecount(name):
    with open(name, 'r') as f:
        lines = f.read()
        return len(lines)
def encode(file):
    m = read(file)
    m = ''.join(m)
    m = base64.b64encode(m)
    overwrite(file, m)
def decode(file):
    m = read(file)
    m = ''.join(m)
    m = base64.b64decode(m)
    overwrite(file, m)
def cleanup(pathto, ext):
    d = path(pathto)
    files = d.walkfiles("*" + ext)
    for file in files:
        file.remove()
def movefiles(bef, ext, aft):
    source = os.listdir(bef)
    for files in source:
        if files.endswith(ext):
            shutil.move(files, aft)
def repline(name, n, m):
    n -= 1
    with open(name, 'r') as f:
        data = f.readlines(n)
        data[n] = m
    with open(name, 'w') as f:
        f.writelines(data)
def findrepl(name, torep, repwith):
    lines = open( name, "r" ).readlines()
    newlines = []
    for line in lines:
        line = re.sub( torep, repwith, line )
        newlines.append(line)
    newlines = ''.join(newlines)
    overwrite(name, newlines)
def getline(name, lookup):
    nums = []
    with open(name) as f:
        for num, line in enumerate(f, 1):
            if lookup in line:
                nums.append(num)
    return nums
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
def delete(name):
    os.remove(name)
def argsettings():
    if sys.argv[1].startswith('--'):
        option = sys.argv[1][2:]
        if option == 'version':
            print ('Versoin 1.0 Public Release!')
        elif option == 'help':
            print ('''\
    Welcome to File.py
    This program has utilities that make it easier to work with fiels in python.
    Options include:
    --version : Prints the version number and exits
    --help    : Prints this help and exits
    --usage   : Prints all the functions available''')
        elif option == 'usage':
            print ('''
Functions:
        1.  write(file, message)          - writes a message to the last line
        2.  singleine(file, line to read) - reads a single line, outputs as string
        3.  read(file)                    - reads all lines in a file as a string
        4.  rlist(file)                   - Returns a list of all the lines of a file
        5.  checkdir(file)                - Checks if a folder exists, if not, create one
        5.  overwrite(file, message)      - overwrites a file with the given message
        6.  eraseall(file)                - erases everything in a file
        7.  newlines(file)                - manages the lines in a file as a multiple of 3
        8.  copy(file1, file2)            - copys the contents of a file to another
        9.  encode(file)                  - encrypts a file using the base64 module
        10.  decode(file)                 - decrypts a file using the base64 module
        11.  singleline(file, line)       - Returns the specified line as a filtered string
        12. charcount(file)               - Returns the character count of a file
        13. linecount(file)               - Returns the line count of a file
        14. repline(file, line, text)     - Replaces line in file with text
        15. findrepl(file, find, replace) - Finds find in file and replaces with replace
        16. getline(file, prhase)         - Returns a list of lines that contain phrase
        17. timesmentioned(file, phrase)  - Returns the number of times the prhase is in file
        18. delete(file)                  - Deletes a file
    
    	There is also a class for strings! its called text(string)
    	functions within it include:
    		1. literal(string)            - Will return an rstring of self.text
    		2. caps(string, mode)         - Can do stuff with capitalization ('switch, title, fix')
    		3. rev(string)                - will reverse the self.text
        ''')
        else:
            print ('Unknown option.')
        sys.exit()
if __name__ == '__main__':
	argsettings()