#!/usr/bin/env python

import traceback, sys

import ConfigParser
import os
import sys
import hashlib
import json
import requests
from urllib3.contrib import pyopenssl
pyopenssl.inject_into_urllib3

import argparse

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
        
bc = bcolors()


class spikenode(object):

  def __init__(self):
    self.parser = self.build_argparser()
    self.args = self.parser.parse_args()
    
    self.config_locations = [
      'spikenode.cfg', 
      os.path.join(os.path.expanduser('~'), '.spikenode.cfg'), 
      '/etc/spikenode.cfg'
    ]

    
  def build_argparser(self):
    parser = argparse.ArgumentParser(description="SpikeNode CLI interface")
    parser.add_argument("--config", help="Location of config file")

    subparsers = parser.add_subparsers(title="command", help="Action to perform", dest="command")

    parser_sync = subparsers.add_parser("upload", help="Upload local directory to your spikenode bucket")
    parser_sync.add_argument("bucket", help="Name of the bucket to upload")
    parser_sync.add_argument("--path", help="Directory to upload (if other than current dir)")

    parser_setup = subparsers.add_parser("setup", help="One-time setup configuration file")
    parser_setup.add_argument("--auth-key", help="API authentication key", dest="auth_token")
    
    return parser

  def hashfile(self, afile, hasher, blocksize=65536): 
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()
    
  def get_command(self):
    return self.args.command

  def msg(self, msg, header=False):
    if header:
      print bc.BOLD + " > " + msg + bc.ENDC
    else:
      print "   " + msg
      
  def fail(self, msg="Oops, something went wrong"):
    sys.exit(bc.FAIL + "   " + msg + bc.ENDC)
  def success(self, msg):
    print bc.OKGREEN + "   " + msg + bc.ENDC
    sys.exit()
  
  def run(self):
    if self.get_command() == "upload":
      self.run_upload()
    elif self.get_command() == "setup":
      self.run_setup()
    else:
      self.fail("Invalid command")
  
  def read_config(self):
    config_file = self.args.config
    
    configParser = ConfigParser.ConfigParser()
    if config_file:
      if not os.path.isfile(config_file):
        self.fail("Could not read config at " + config_file)

      self.config_locations.insert(0, config_file)

    try: 
      configParser.read(self.config_locations)
    except: 
      self.fail('Could not read config file, run setup to create one')
      
    try: 
      self.token = configParser.get('auth', 'key')
    except:
      self.fail('API authentication key is not defined')

    try: 
      api = configParser.get('defaults', 'endpoint')
    except: 
      api = "https://app.spikenode.com/api"
  
    # Endpoints
    self.api_sync = api + "/sync"
    self.api_upload = api + "/sync/upload"
    self.api_end = api + "/sync/end"
  
  def run_upload(self):
    bucket = self.args.bucket
    path = self.args.path or "."
    
    self.read_config()
  
    try:
      os.chdir(path)
    except:
      self.fail("Could not change dir to path: " + path)

    files = []
    for root, dirnames, filenames in os.walk("."):
      for filename in filenames:
        file = os.path.join(root, filename)
        hash = self.hashfile(open(file, 'rb'), hashlib.md5())
        files.append(file.replace("\\","/").replace("./","") + '.' + hash)
        
    # First Request to check what needs to be sent
    try:
      r = requests.post(self.api_sync + "?access_token=" + self.token, json={"bucket": bucket, "files": files});
    except Exception, e:
      print(traceback.format_exc())
      self.fail("Could not contact API endpoint at " + self.api_sync + ". Check your connection.")

    if r.status_code == 400:
      self.fail("Bucket does not exist")

    try:
      filesToSend = json.loads(r.text)['files']
    except:
      self.fail("Fail to read API response, check your API key")

    if len(filesToSend) == 0:
      return self.success("All files synchronized with server")
      
    # Second request with actual files
    for fileToSend in filesToSend:
      filename = fileToSend.rsplit('.', 1)[0]
      self.msg("UPLOADING: "+ filename)
      postFile = {fileToSend: (fileToSend, open(filename, 'rb'))}
      try:
        r = requests.post(self.api_upload + "?access_token=" + self.token, files=postFile, data={"bucket": bucket})
      except:
        self.fail("Could not upload file to endpoint, check your connection.")
      if r.status_code != 200:
        self.fail("Could not upload file to endpoint, check your connection.")

    # Third request to wrap up connection and notify user
    r = requests.post(self.api_end + "?access_token=" + self.token, json={"bucket": bucket })
    
    self.success("Upload completed")

  def run_setup(self):
    auth_token = ""
    if hasattr(self.args, 'auth_token') and self.args.auth_token != None:
      auth_token = self.args.auth_token
    else:
      self.msg("Setup Authentication", True)
      self.msg("Please provide your API key to use this CLI.")
      self.msg("You can create one at the Profile section in SpikeNode.")
      auth_token = raw_input("  Key: ")
      
    config_file = os.path.join(os.path.expanduser("~"), ".spikenode.cfg") # TODO: move to home
    parser = ConfigParser.ConfigParser()
    parser.add_section("auth")
    parser.set("auth", "key", auth_token)
    
    afile = open(config_file, "w")
    parser.write(afile)
    afile.close()
    self.success("> Config file created at " + config_file)
    
def main():
    """Entrypoint for the CLI app"""
    
    if os.name == "nt":
      bc.disable()

    sn = spikenode()
    sn.run()

if __name__ == '__main__':
    main()
