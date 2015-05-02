__author__ = 'Jake'
#Import modules
import sys, pickle, os, zipfile, subprocess
from easygui import *
from time import gmtime, strftime

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

def pipupgrade():
    import pip

    for dist in pip.get_installed_distributions():
        subprocess.call("pip install --upgrade " + dist.project_name, shell=True)

def upgrade():
    subprocess.call("pip install --upgrade jpt", shell=True)

def cmd(cmdcommand):
    subprocess.call(cmdcommand, shell=True)