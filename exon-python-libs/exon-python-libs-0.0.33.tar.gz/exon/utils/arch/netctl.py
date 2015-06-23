__author__ = 'Stephan Conrad <stephan@conrad.pics>'

from pathlib import Path
from exon.utils.fileutils import readfile, writefile, writefileFromArray
from exon.utils.command.execute import exec as run
import os
import re

_SUPPORTED_CONNECTIONS = (
    'bond',
    'bridge',
    'ethernet',
    'macvlan',
    'mobile_ppp',
    'openvswitch',
    'pppoe',
    'tunnel',
    'tuntap',
    'vlan',
    'wireless',
)

class NetFieldErrorException(Exception):
    def __init__(self, message=None, fieldMessages={}, *args, **kwargs):
        self.fieldMessages = fieldMessages
        super().__init__(message, *args, **kwargs)

    def hasErrors(self):
        return len(self.fieldMessages) >= 1


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
        ret = {}
        if map['enabled'] != dev.enabled:
            dev.enabled = map['enabled']
            dev.changed['enabled'] = None
        for key in map['config']:
            ret[key] = {
                'value':map['config'][key],
                'type': str(type(map['config'][key]))
            }
        error = NetFieldErrorException(message='Error in JSON fields')

        if type(map['config']['dns']) == list:
            dev.dns = map['config']['dns']
        else:
            error.fieldMessages['dns'] = 'Must be a list'

        if type(map['config']['routes6']) == list:
            dev.routes6 = map['config']['routes6']
        else:
            error.fieldMessages['routes6'] = 'Must be a list'

        if type(map['config']['address']) == list:
            dev.address = map['config']['address']
            test = re.compile('^(\d{0,3})\.(\d{0,3})\.(\d{0,3})\.(\d{0,3})(\/)(\d{1,2})$')
            ret['debug'] = []
            for a in map['config']['address']:
                if test.search(a) == None:
                    ret['debug'].append(a)
                    error.fieldMessages['address'] = 'Must be in form xxx.xxx.xxx.xxx/xx'
                    ret['debug'].append(len(error.fieldMessages))
        else:
            error.fieldMessages['address'] = 'Must be a list'

        if type(map['config']['routes']) == list:
            dev.routes = map['config']['routes']
        else:
            error.fieldMessages['routes'] = 'Must be a list'

        if type(map['config']['address6']) == list:
            dev.address6 = map['config']['address6']
        else:
            error.fieldMessages['address6'] = 'Must be a list'

        if type(map['config']['gateway']) == str:
            dev.gateway = map['config']['gateway']
        else:
            error.fieldMessages['gateway'] = 'Must be a string'

        if type(map['config']['gateway6']) == str:
            dev.gateway6 = map['config']['gateway6']
        else:
            error.fieldMessages['gateway6'] = 'Must be a string'

        if type(map['config']['connection']) == str:
            if map['config']['connection'] not in _SUPPORTED_CONNECTIONS:
                error.fieldMessages["connection"] = 'Must be one of: %s' % ", ".join(_SUPPORTED_CONNECTIONS)
            else:
                dev.connection = map['config']['connection']
        else:
            error.fieldMessages['connection'] = 'Must be a string'

        if type(map['config']['interface']) == str:
            dev.interface = map['config']['interface']
        else:
            error.fieldMessages['interface'] = 'Must be a string'

        if type(map['config']['ip']) == str:
            if map['config']['ip'] in ('static', 'dhcp'):
                dev.ip = map['config']['ip']
            else:
                error.fieldMessages['ip'] = "Must be static or dhcp"
        else:
            error.fieldMessages['ip'] = 'Must be a string'

        if type(map['config']['description']) == str:
            dev.description = map['config']['description']
        else:
            error.fieldMessages['description'] = 'Must be a string'

        if type(map['config']['ip6']) == str:
            if map['config']['ip6'] in ('static', 'dhcp', 'stateless', 'yes'):
                dev.ip6 = map['config']['ip6']
            else:
                error.fieldMessages['ip6'] = "Must be static, yes, stateless or dhcp"
        else:
            error.fieldMessages['ip6'] = 'Must be a string'

        if error.hasErrors():
            raise error
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
        self.mac = ""
        self.changed = {}
        if cfgfile != None:
            self._parseFile(cfgfile)
            self.name = os.path.basename(cfgfile)
            self._cfgFile = cfgfile
        elif name != None:
            cfgfile = os.path.join(basepath, name)
            if os.path.isfile(cfgfile):
                self._parseFile(cfgfile)
            self.name = name
            self._cfgFile = cfgfile
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

    def write(self):
        lines = []
        lines.append("Description='%s'" % self.description.strip('\'"'))
        lines.append('Interface=%s' % self.interface)
        lines.append('Connection=%s' % self.connection)
        if self.ip != "":
            lines.append('IP=%s' % self.ip)
        if len(self.address) > 0:
            lines.append('Address=(%s)' % ' '.join(["'%s'" % x for x in self.address]))
        if len(self.routes) > 0:
            lines.append('Routes=(%s)' % ' '.join(["'%s'" % x for x in self.routes]))
        if self.dns != "":
            lines.append("Gateway='%s'" % self.gateway)
        if len(self.address) > 0:
            lines.append("DNS=(%s)" % ' '.join(["'%s'" % x for x in self.dns]))
        if self.ip6 != "":
            lines.append("IP6=%s" % self.ip6)
        if len(self.address6) > 0:
            lines.append("Address6=(%s)" % ' '.join(["'%s'" % x for x in self.address6]))
        if len(self.routes6) > 0:
            lines.append("Routes6=('%s')" % ' '.join(["'%s'" % x for x in self.routes6]))
        if self.gateway6 != "":
            lines.append("Gateway6='%s'" % self.gateway6)

        writefileFromArray(self._cfgFile, lines)

    def _runNetCtl(self, command):
        cmd = 'netctl %s %s' % (command, self.name)
        out = run(cmd)
        self._lastError = out
        self._lassCommand = cmd
        return out.rc == 0

    def restart(self):
        return self._runNetCtl("restart")

    def start(self):
        return self._runNetCtl("start")

    def stop(self):
        return self._runNetCtl("stop")

    def enable(self):
        return self._runNetCtl("enable")

    def disable(self):
        return self._runNetCtl("disable")

    def enableOrDisable(self):
        if 'enabled' in self.changed:
            if self.enabled:
                return self.enable()
            else:
                return self.disable()
        return True

class Netdev(object):
    def __init__(self, dev):
        self.dev = dev
        self._getData()

    def _getData(self):
        self.ip = []
        self.ip6 = []
        out = run('ip addr show dev {}'.format(self.dev))
        if out.rc == 0:
            for line in out.stdout:
                line = line.strip()
                if line.startswith("link/ether"):
                    self.mac = line.split(" ")[1]
                elif line.startswith("inet "):
                    self.ip.append(line.split(" ")[1])
                elif line.startswith("inet6 "):
                    self.ip6.append(line.split(" ")[1])


if __name__ == "__main__":
    netctl = Netctl()
    ret = NetctlInterface.fromApiJson({
    "config": {
        "gateway6": "",
        "routes6": [],
        "gateway": "192.168.2.1",
        "description": "'Interface eth1'",
        "address": ["192.168.2.100/24", "192.168.3.100/24"],
        "address6": [],
        "ip6": "stateless",
        "routes": ["192.168.2.0/24 via 192.168.2.1", "192.168.3.0/24 via 192.168.3.1"],
        "dns": ["192.168.2.1"],
        "connection": "ethernet",
        "ip": "static",
        "interface": "eth1"
    },
    "name": "eth1",
    "current": {
        "dns": [
            "192.168.106.2"
        ],
        "status": "up",
        "routes": {
            "192.168.106.0/24": "eth0",
            "default": "192.168.106.2"
        },
        "ip": [
            "192.168.106.150/24"
        ],
        "ip6": [
            "fe80::20c:29ff:fe14:3d7c/64"
        ],
        "mac": "00:0c:29:14:3d:7c"
    },
    "enabled": True
})
    print(ret.write())