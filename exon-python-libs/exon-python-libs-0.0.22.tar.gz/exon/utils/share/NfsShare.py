__author__ = 'Stephan Conrad <stephan@conrad.pics>'

from os import listdir
from os.path import isfile, join
from exon.utils.share import ShareService, Share, Acl
from exon.utils.fileutils import readfileAsArray, writefileFromArray
from exon.utils.command.execute import exec as run
import re

class NfsShare(Share):
    """
    Extended Share class for NFS Shares
    """
    def __init__(self, name=None, path=None, acl=Acl(), options={}, sourceFile = {}):
        super().__init__(name, path, acl, options)
        self.type = 'nfs'
        self.options = options
        self.sourceFile = sourceFile

    def toJson(self):
        ret = {
            'write_hosts': [],
            'read_hosts': []
        }
        for server in self.acl.read:
            ret['read_hosts'].append(server)
        for server in self.acl.write:
            ret['write_hosts'].append(server)
        return ret

    def __repr__(self):
        return '{name: %s, path: %s, acl: %s, options: %s, sourceFile: %s}' % (self.name, self.path, self.acl, self.options, self.sourceFile)

    @classmethod
    def fromJson(cls, map):
        share = cls(acl = Acl(write=map['write_hosts'], read=map['read_hosts']))
        return share


class NfsShareService(ShareService):
    _EXPORT_CONFIG_FILE = '/etc/exports'
    def __init__(self):
        self._exportFiles = [self._EXPORT_CONFIG_FILE]
        self._reloadCMD = 'exportfs -ar'
        for f in listdir('/etc/exports.d'):
            file = join('/etc/exports.d',f)
            if isfile(file):
                self._exportFiles.append(file)

    def getShares(self):
        shares = {}
        for file in self._exportFiles:
            for line in readfileAsArray(file):
                line = line.strip()
                if line != '' and not line.startswith('#'):
                    (path, server) = re.split('\s+', line, 1)
                    if len(path) > 1 and path[0]:
                        path = "".join(path[1:])
                    name = path.replace('/', '__')
                    (servername, optionString) = server.replace('(', ' ').replace(')','').split(' ', 1)
                    if '#' in optionString:
                        (optionString, comments) = optionString.split('#', 1)
                        for comment in comments.split(';'):
                            (key, val) = comment.split('=', 1)
                            key = key.strip()
                            val = val.strip()
                            if key == 'exon_name':
                                name = val
                    options = optionString.split(',')
                    rw = []
                    ro =[]
                    if "rw" in options:
                        rw.append(servername)
                    else:
                        ro.append(servername)
                    share = None
                    if name not in shares:
                        share = NfsShare(
                            name = name,
                            path = "/%s" % path,
                            acl=Acl(read=ro, write=rw),
                            options={servername: options},
                            sourceFile={servername: file}
                        )
                    else:
                        share = shares[name]
                        for s in ro:
                            share.acl.read.append(s)
                        for s in rw:
                            share.acl.write.append(s)
                        share.options[servername] = options
                        share.sourceFile[servername] = file
                    shares[name] = share
        return shares

    def writeShare(self, share):
        oldShares = self.getShares()
        hosts = []
        for host in share.acl.read:
            hosts.append(host)
        for host in share.acl.write:
            hosts.append(host)
        if len(share.options) == 0:
            if share.name in oldShares:
                share.options = oldShares[share.name].options
                share.sourceFile = oldShares[share.name].sourceFile
        for host in hosts:
            if host not in share.options:
                share.options[host] = ['sync', 'fsid=0', 'ro']
        for key in share.options:
            newOptions = []
            serverAccess = ''
            if key in share.acl.write:
                serverAccess = 'rw'
            if key in share.acl.read:
                serverAccess = 'ro'
            for option in share.options[key]:
                option = option.strip()
                if option in ('rw', 'ro'):
                    option = serverAccess
                if option not in newOptions and option != '':
                    newOptions.append(option)
            shareLine = '%s\t%s(%s) # exon_name=%s' % (
                share.path,
                key,
                ','.join(newOptions),
                share.name
            )
            newServer = False
            if key not in share.sourceFile:
                share.sourceFile[key] = self._EXPORT_CONFIG_FILE
                newServer = True
            regex = re.compile('%s\s+?%s\(.+?\)\s*?' % (share.path, key))
            fileLines = readfileAsArray(share.sourceFile[key])
            if not newServer:
                for i in range(0, len(fileLines)):
                    match = regex.search(fileLines[i])
                    if match:
                        fileLines[i] = shareLine
            else:
                fileLines.append(shareLine)
            writefileFromArray(share.sourceFile[key], fileLines)
        out = run(self._reloadCMD)
        return bool(out.rc == 0)

    def fromJson(self, map):
        return NfsShare.fromJson(map)

    def delete(self, name):
        shares = self.getShares()
        share = shares[name]
        for file in set(share.sourceFile.values()):
            newLines = []
            regex = re.compile('.+?\s+?.+?\s*?\(.+?\)\s*?#.*?exon_name=(.+?)(;|$)')
            for line in readfileAsArray(file):
                match = regex.search(line)
                if match:
                    if len(match.groups()) >= 1:
                        if not match.group(1) == name:
                            newLines.append(line)
                        else:
                            pass
                    else:
                        newLines.append(line)
                else:
                    newLines.append(line)
            writefileFromArray(file, newLines)
        out = run(self._reloadCMD)
        return bool(out.rc == 0)
