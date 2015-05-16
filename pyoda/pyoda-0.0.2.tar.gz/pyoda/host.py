
import platform
import socket
import subprocess
import time
import re
import os
import json

import pyoda.request

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

class Host(object):

  def __init__(self, org, hid = "0"):
    self.__org = org
    self.data = {
        "id": hid,
        "unique_id": "",
        "instance_id" : "",
        "image_id": "",
        "instance_name": "",
        "ip_v4": "",
        "launch_time": "",
        "name": "",
        "state": "",
        "type": "",
        "url": "",
        "zone": "",
        "description": "",
        }

  def __getHostType(self):
    system = platform.system()
    if system == "Darwin":
      return self.__getDarwinHostType()
    elif system == "Linux":
      return self.__getLinuxHostType()
    else:
      raise Exception( "Platform {0} not supported".format( system ) )

  def __getDarwinHostType(self):
    cpu_name = ""
    ncores = ""
    mem = 0
    for line in  subprocess.Popen(['sysctl', '-a'], stdout=subprocess.PIPE).communicate()[0].split("\n"):
      fields = [ f.strip() for f in line.split(":") if f.strip() ]
      if not fields:
        continue
      if fields[0] == "machdep.cpu.core_count":
        ncores = fields[1]
      elif fields[0] == "machdep.cpu.brand_string":
        cpu_name = fields[1]
      elif fields[0] == "hw.memsize":
        mem = int( fields[1] ) / (1024**3)
    return "{}x{} ({} GB)".format( ncores, cpu_name, mem)

  def __getLinuxHostType(self):
    cpu_name = ""
    ncores = ""
    with open( "/proc/meminfo" ) as f:
      fields = [ e.strip() for e in f.readline().split() if e.strip() ]
      mem = int(fields[1]) / 1024 / 1024
    with open( "/proc/cpuinfo" ) as f:
      for line in f.readlines():
        fields = [ e.strip() for e in line.split(":") if e.strip() ]
        if len(fields) < 2:
          continue
        if fields[0] == "model name":
          cpu_name = fields[1]
        elif fields[0] == "processor":
          ncores = fields[1]
    return "{}x{} ({} GB)".format( ncores, cpu_name, mem)


  def autoFill(self):
    self.data.update( {
      "image_id": platform.platform(),
      "instance_name": socket.getfqdn(),
      "ip_v4": [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1],
      "launch_time": time.strftime( "%Y/%m/%d %H:%M:%S", time.localtime(os.path.getctime("/etc/bashrc"))),
      "name": socket.gethostname(),
      "state": "running",
      "type": self.__getHostType(),
      "url": "ssh://root@{}".format(socket.getfqdn() ),
      "zone": "datacenter 1",
      "description": "Autofilled with love :)"
      })

  def fillFromDict( self, odata ):
    for k in self.data:
      try:
        self.data[k] = odata[k]
      except KeyError:
        pass

  def saveAsManualHost(self):
    self.fillFromDict( pyoda.request.post( self.__org, self.__org.url("host"), self.data ) )

  def getSecrets(self):
    self.__org.crypto.retrieveCSKeys()
    secrets = pyoda.request.get( self.__org, self.__org.url( "host/{id}/ciphertext".format( **self.data ) ) )
    if len( secrets ) == 0:
      return {}
    try:
      ciphertext = secrets[0][ 'ciphertext' ]
    except KeyError:
      return {}
    groupKey = self.__org.crypto.decryptWithSession(secrets[0]['private_key'])
    key = pyoda.crypto.Key( groupKey )
    return json.loads( key.decryptWithSession( ciphertext ) )

  def __str__(self):
    return json.dumps( self.data )
