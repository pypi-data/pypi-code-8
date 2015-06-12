__author__ = 'Stephan Conrad <stephan@conrad.pics>'

from pathlib import Path
from exon.utils.fileutils import readfile, writefile
from exon.utils.command.execute import exec, CommandOut
import os
import re

def getAllNics():
    ret = []
    get_if_cmd = 'ip link|grep -v lo'
    for line in os.popen(get_if_cmd):
        if re.match("^\d", line):
            s = line.split(":")
            name = s[1].strip();
            ret.append(name)
    return ret

class Netdev(object):
    def __init__(self, dev):
        self.dev = dev
        self._getData()

    def _getData(self):
        self.ip = []
        self.ip6 = []
        out = exec("ip addr show dev {}".format(self.dev))
        if out.rc == 0:
            for line in out.stdout:
                line = line.strip()
                if line.startswith("link/ether"):
                    self.mac = line.split(" ")[1]
                elif line.startswith("inet "):
                    self.ip.append(line.split(" ")[1])
                elif line.startswith("inet6 "):
                    self.ip6.append(line.split(" ")[1])

class Netctl(object):
    def __init__(self):
        self.config_path = "/etc/netctl"
        self.interfaces = []
        self._getInterfaces()
        print(self.interfaces)

    def _getInterfaces(self):
        path = Path(self.config_path)
        for file in path.iterdir():
            if file.is_file():
                self.interfaces.append(file.name)

    def getInterface(self, name):
        cfile = os.path.join(self.config_path, name)
        if os.path.exists(cfile):
            return NetctlInterface(cfile=cfile, name=name)

class NetctlInterface(object):
    def __init__(self, cfile = None, name = None, basepath = "/etc/netctl"):
        if cfile != None:
            self._parseFile(cfile)
        elif name != None:
            pass
        else:
            return
        self._getIpInfo(name)

    def _getIpInfo(self, name):
        ipOut = exec("ip addr show {}".format(name))
        self.ipaddress = []
        self.ipaddress6 = []
        for line in ipOut.stdout:
            temp = line.strip()
            if temp.startswith("link/ether"):
                self.mac = temp.split(" ")[1]
            elif temp.startswith("inet "):
                self.ipaddress.append(temp.split(" ")[1])
            elif temp.startswith("inet6"):
                self.ipaddress6.append(temp.split(" ")[1])

    def _parseFile(self,cfile):
        lines = readfile(cfile).split("\n")
        for line in lines:
            if not line.startswith("#"):
                if line.count("=") >= 1:
                    t = line.split("=")
                    if len(t) >= 2:
                        key = t[0]
                        value = "".join(t[1:])
                        if key == "Description":
                            self.description = value
                        elif key == "Interface":
                            self.interface = value
                        elif key == "Connection":
                            self.connection = value
                        elif key == "IP":
                            self.ip = value
                        elif key == "IP6":
                            self.ip6 = value
                        elif key == "Address":
                            self.address = value.replace("(", "").replace(")", "").replace("'", "").split(" ")
                        elif key == "Routes":
                            self.routes = ";".join(value.replace("(", "").replace(")", "").split("' '")).replace("'", "").split(";")
                        elif key == "Gateway":
                            self.gateway = value
                        elif key == "DNS":
                            self.dns = value.replace("(", "").replace(")", "").replace("'", "").split(" ")
                        elif key == "Address6":
                            self.address6 = value.replace("(", "").replace(")", "").replace("'", "").split(" ")
                        elif key == "Routes6":
                            self.routes6 = ";".join(value.replace("(", "").replace(")", "").split("' '")).replace("'", "").split(";")
                        elif key == "Gateway6":
                            self.gateway6 = value



if __name__ == "__main__":
    netctl = Netctl()
    print(netctl.getInterface("eth0").ipaddress)