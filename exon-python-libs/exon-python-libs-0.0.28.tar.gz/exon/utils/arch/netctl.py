__author__ = 'Stephan Conrad <stephan@conrad.pics>'

from pathlib import Path
from exon.utils.fileutils import readfile, writefile
from exon.utils.command.execute import exec as run
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

class Netctl(object):
    """
    Class for managing Netclt configuration
    """
    def __init__(self):
        self.config_path = "/etc/netctl"
        self.interfaces = []
        self._getInterfaces()

    def _getInterfaces(self):
        netctl = run('netctl list')
        for line in netctl.stdout:
            line = line.strip()
            if line != '':
                if '*' in line:
                    line = line.replace('*', '').strip()
                self.interfaces.append(line)

    def getAllInterfaces(self):
        """
        Lists all Interfaces
        :return: list of interfaces
        """
        return self.interfaces

    def getInterface(self, name):
        """
        Reads the config for an interface
        :param name: interface configuration name
        :return: a NetctlInterface object for the selected interface
        """
        cfile = os.path.join(self.config_path, name)
        if os.path.exists(cfile):
            return NetctlInterface(cfgfile=cfile, name=name)

class NetctlInterface(object):

    @classmethod
    def fromApiJson(cls, map):
        dev = cls(name = map['name'])
        return dev

    def __init__(self, cfgfile = None, name = None, basepath = "/etc/netctl"):
        self.description = ""
        self.interface = ""
        self.connection = ""
        self.ip = ""
        self.ip6 = ""
        self.address = []
        self.routes = []
        self.gateway = ""
        self.dns = []
        self.address6 = []
        self.routes6 = []
        self.gateway6 = ""
        self.enabled = False
        self.ipaddress = []
        self.ipaddress6 = []
        self.current_dns = []
        self.current_route = {}
        if cfgfile != None:
            self._parseFile(cfgfile)
        elif name != None:
            cfgfile = os.path.join(basepath, name)
            if os.path.isfile(cfgfile):
                self._parseFile(cfgfile)
        else:
            return
        self._getIpInfo(self.interface)

    def _getIpInfo(self, name):
        ipOut = run("ip addr show {}".format(name))
        statusRegexString = "\d+: {}: <.+> .+state (.+?)\s+".format(name)
        statusRegex = re.compile(statusRegexString)
        self.status = 'down'
        for line in ipOut.stdout:
            temp = line.strip()
            if statusRegex.match(line):
                r = statusRegex.search(line)
                groups = r.groups()
                if len(groups) >= 1:
                    self.status = groups[0].lower()
            if temp.startswith("link/ether"):
                self.mac = temp.split(" ")[1]
            elif temp.startswith("inet "):
                self.ipaddress.append(temp.split(" ")[1])
            elif temp.startswith("inet6"):
                self.ipaddress6.append(temp.split(" ")[1])
        routeOut = run('ip route show dev %s' % name)
        if routeOut.rc == 0:
            for line in routeOut.stdout:
                fields = re.split('\s+', line)
                if line.startswith('default'):
                    self.current_route['default'] = fields[2]
                elif line != '':
                    self.current_route[fields[0]] = name
        dnsOut = run("resolvconf -l '%s*'" % name)
        if dnsOut.rc == 0:
            for line in dnsOut.stdout:
                if line.startswith('nameserver'):
                    server = re.split('\s+', line)[1]
                    self.current_dns.append(server)

    def _parseFile(self, cfgfile):
        lines = readfile(cfgfile).split("\n")
        file = os.path.basename(cfgfile)
        enabled = run('netctl is-enabled %s' % file)
        self.enabled = bool(enabled.rc == 0)
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
    print(netctl.getInterface("eth0").status)
    print(netctl.getInterface("eth1").status)