#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, time, sys ,ConfigParser,platform,urllib
import pyimgur
import sys
import pyperclip
from os.path import expanduser

homedir = expanduser("~")
config = ConfigParser.RawConfigParser()
config.read(homedir+'/imgur.cfg')


try:
	CLIENT_ID = config.get('imgur', 'CLIENT_ID')
	im = pyimgur.Imgur(CLIENT_ID)
	path_to_watch = config.get('config', 'path_to_watch')
except ConfigParser.NoSectionError, err:
    print 'Error Config File:', err

def setCodeingByOS():
    '''获取系统平台,设置编解码'''
    if 'cygwin' in platform.system().lower():
        CODE = 'GBK'
    elif os.name == 'nt' or platform.system() == 'Windows':
        CODE = 'GBK'
    elif os.name == 'mac' or platform.system() == 'Darwin':
        CODE = 'utf-8'
    elif os.name == 'posix' or platform.system() == 'Linux':
        CODE = 'utf-8'
    return  CODE

def set_clipboard(url_list):
	for url in url_list:
		pyperclip.copy(url)
	spam = pyperclip.paste()

def main():
    print "running ... ..."
    before = dict([(f, None) for f in os.listdir(path_to_watch)])
    while 1:
        time.sleep(1)
        after = dict([(f, None) for f in os.listdir(path_to_watch)])
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        if added:
            print "Added Files: ", ", ".join(added)
            url_list = []
            for i in added:
				uploaded_image = im.upload_image(os.path.join(path_to_watch, i), title=i.decode(setCodeingByOS()))
				url_list.append(uploaded_image.link)
            print uploaded_image.link
            set_clipboard(url_list)
        if removed:
            print "Removed Files: ", ", ".join(removed)
            print  removed
        before = after

if __name__ == "__main__":
	main()


