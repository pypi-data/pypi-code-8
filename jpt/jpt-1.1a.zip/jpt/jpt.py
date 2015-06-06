__author__ = 'Jake'
#Import modules
import sys, pickle, os, zipfile, subprocess, gui
from time import gmtime, strftime
import time as time2
import binascii

#Defining vars
pkgnm = None

#Functions
def dt():
    return (strftime("%Y-%m-%d %H:%M:%S", gmtime()))

def time():
    return (strftime("%H:%M:%S", gmtime()))

def date():
    return (strftime("%Y-%m-%d", gmtime()))

def datenodash():
    return (strftime("%Y %m %d", gmtime()))

def dtnodash():
    return (strftime("%Y %m %d %H:%M:%S", gmtime()))

def dtforwardslash():
    return (strftime("%Y/%m/%d %H:%M:%S", gmtime()))

def dateforwardslash():
    return (strftime("%Y/%m/%d", gmtime()))

def username():
    username = os.environ.get( "USERNAME" )
    return username

def caps(string):
    return string.capitalize()

def title(string):
    return string.title()

def lower(string):
    return string.lower()

def upper(string):
    return string.upper()

def capsp(string):
    print(string.capitalize())

def titlep(string):
    print(string.title())

def lowerp(string):
    print(string.lower())

def uppep(string):
    print(string.upper())

def save(whattosave, nameoffile):
    pickle.dump(whattosave, open(nameoffile, "wb"))

def load(whattoload):
    return pickle.load(open(whattoload, "rb"))

def join(firststring, secondstring):
    return firststring + secondstring

def joinp(firststring, secondstring):
    print(firststring + secondstring)

def nonum(string):
    string = string.replace('1', '')
    string = string.replace('2', '')
    string = string.replace('3', '')
    string = string.replace('4', '')
    string = string.replace('5', '')
    string = string.replace('6', '')
    string = string.replace('7', '')
    string = string.replace('8', '')
    string = string.replace('9', '')
    return string

def zip(zipfilename, whattozip):
    zf = zipfile.ZipFile(zipfilename, mode='w')
    try:
        zf.write(whattozip)
    finally:
        zf.close()

def unzip(zipname, place=(os.path.dirname(os.path.realpath(__file__)))):
    with zipfile.ZipFile(zipname) as zf:
        zf.extractall(place)

def playmp3(song):
    try:
        os.startfile(song)
    except:
        print("Error, Is your system windows?")

def isprime(n):
    n = abs(int(n))
    if n < 2:
        return False
    if n == 2:
        return True
    if not n & 1:
        return False
    for x in range(3, int(n**0.5)+1, 2):
        if n % x == 0:
            return False
    return True

def pipupgrade(response2="Done", Silent=False):
    import pip
    try:
        for dist in pip.get_installed_distributions():
            subprocess.call("pip install --upgrade " + dist.project_name + " -q", shell=True)
            if Silent:
                pass
            else:
                print("Checked Package, " + dist.project_name)
        if Silent:
            pass
        else:
            print(response2)
    except:
        print("Admin privilages might be required")

def upgrade():
    subprocess.call("pip install --upgrade jpt", shell=True)

def cmd(cmdcommand):
    subprocess.call(cmdcommand, shell=True)

def tobinary(s_str):
    binary = []
    for s in s_str:
        if s == ' ':
            binary.append('00100000')
        else:
            binary.append(bin(ord(s)))
        binary.append(' ')
    b_str = '\n'.join(str(b_str) for b_str in binary)
    b_str = b_str.replace('b','')
    b_str = b_str.replace('\n','')
    return b_str

def toascii(string):
    bstr = string.replace(' ','')
    n = int(bstr, 2)
    a_str = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    return a_str

def write(nameoffile, whattowrite):
    file = open(nameoffile,'w')   # Trying to create a new file or open one
    file.write(whattowrite)
    file.close()

def speak(string):
    write('temp.bat', '''
@echo off

set text=''' + string + '''

rem Making the temp file
:num
set num=%random%
if exist temp%num%.vbs goto num
echo ' > "temp%num%.vbs"
echo set speech = Wscript.CreateObject("SAPI.spVoice") >> "temp%num%.vbs"
echo speech.speak "%text%" >> "temp%num%.vbs"
start temp%num%.vbs

    ''')
    cmd('temp')
    time2.sleep(0.5)
    cmd('del temp.bat')

    for root ,dirs, files in os.walk(os.getcwd()):
        for currentFile in files:
            exts=('.vbs')
            exts2=('temp')
            if any(currentFile.lower().endswith(ext) for ext in exts):
                if any(currentFile.lower().startswith(ext) for ext in exts2):
                    os.remove(os.path.join(root, currentFile))


#Command line use
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--pipupgrade', '-pu',
    action='store_true',
    help='Pip Upgrade Flag' )

args = parser.parse_args()

if args.pipupgrade:
    pipupgrade()
else:
    pass




