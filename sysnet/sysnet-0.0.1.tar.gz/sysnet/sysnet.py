#! /usr/bin/python
import os
import re
import sys
import ssl
import json
import time
import copy
import socket
import urllib
import Cookie
import thread
import urllib
import base64
import httplib
import argparse
import datetime
import traceback
import mimetypes
import SimpleHTTPSServer


__version__ = "0.0.1"
__description__ = "Server Administrator"
__logo__ = """
                     _       _
                    | |     | |
 ___ _   _ ___ _ __ | |_ ___| |_
/ __| | | / __| '_ \\| __/ _ \\ __|
\\__ \\ |_| \\__ \\ | | | ||  __/ |_
|___/\\__, |___/_| |_|\\__\\___|\\__|
      __/ |
     |___/
"""
PORT = 7342

def main():
    address = "0.0.0.0"

    port = PORT
    if len(sys.argv) > 1:
        port = int(sys.argv[1])


if __name__ == '__main__':
    main()
