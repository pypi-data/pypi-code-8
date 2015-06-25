# -*- coding: utf-8 -*-
#/usr/bin/python
'''
Created on 2015-06-24 12:42
@summary: Simple Encode Image To string
@author: LICFACE
@email: licface13@gmail.com 
@url: http://www.licface.tk
'''


import base64
import argparse
import sys
import os
import clip

class encode(object):
    '''
    @summary: Encode Class
    '''
    def __init__(self):
        '''
        @summary: Initialize
        @result: None
        '''
        super(encode, self)
        self.clip = clip.clipboard()

    def encode_image(self, image, copy=None, filename=None):
        '''
        @summary: Encode Base64 from image file
        @param image: file
        @result: str base64
        '''
        with open(image, 'rb') as imagefile:
            str = base64.b64encode(imagefile.read())
            if copy:
                self.clip = clip.clipboard(str)
            if filename:
                filename.write(str)
            print str
            return str

    def usage(self):
        '''
        @summary: Usage Command line helper
        @result: str usage help
        '''
        parser = argparse.ArgumentParser()
        parser.add_argument('-m', '--image', help='Image path', action='store')
        parser.add_argument('-c', '--copy', help='Copy string out/result to clipboard', action='store_true')
        parser.add_argument('-f', '--file', help='Store string out/result to file', action='store', dest='filename', type=argparse.FileType('w'))
        if len(sys.argv) == 1:
            parser.print_help()
        elif os.path.isfile(sys.argv[1]):
            parser.print_help()
        else:
            args = parser.parse_args()
            self.encode_image(args.image, args.copy, args.filename)

if __name__ == "__main__":
    c = encode()
    c.usage()