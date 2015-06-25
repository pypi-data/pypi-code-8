# -*- coding: utf-8 -*-
#/usr/bin/python
'''
Created on 2015-06-24 12:42
@summary: Simple Decode Image From string To File
@author: LICFACE
@email: licface13@gmail.com 
@url: http://www.licface.tk
'''


import base64
import argparse
import sys
import os
import encode

class decode(object):
    '''
    @summary: Decode Class
    '''
    def __init__(self):
        '''
        @summary: initialize
        @result: None
        '''
        super(decode, self)
        self.encode = encode.encode()

    def decode_image(self, image, image_out, imgstr=None):
        '''
            @summary: Decode Base64 from image String
            @param image: file
            @param image_out: file
            @param imgstr: str
            @result: file
        '''
        if imgstr == None:
            imgstr = self.encode.encode_image(image)
        if os.path.splitext(image_out)[1] == '':
            image_out = image_out + os.path.splitext(str(image))[1]

        with open(image_out, 'wb') as imagefile:
            imagefile.write(imgstr.decode('base64'))
            imagefile.close()

    def usage(self):
        '''
            @summary: Usage Command line helper
            @result: str usage help
        '''
        parser = argparse.ArgumentParser()
        parser.add_argument('-m', '--image', help='Image path', action='store')
        parser.add_argument('-o', '--image-out', help='Save to Image path', action='store')
        parser.add_argument('-s', '--string', help='String Image have being encode', action='store')
        if len(sys.argv) == 1:
            parser.print_help()
        elif os.path.isfile(sys.argv[1]):
            parser.print_help()
        else:
            args = parser.parse_args()
            if args.image_out:
                self.decode_image(args.image, args.image_out, args.string)
            else:
                parser.print_help()

if __name__ == "__main__":
    c = decode()
    c.usage()