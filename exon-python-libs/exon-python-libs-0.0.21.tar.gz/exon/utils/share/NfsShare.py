__author__ = 'Stephan Conrad <stephan@conrad.pics>'

from os import listdir
from os.path import isfile, join
from exon.utils.share import ShareService, Share, Acl
from exon.utils.fileutils import readfileAsArray, writefileFromArray
import re

class NfsShare(Share):
    def __init__(self, name=None, path=None, acl=Acl, options={}):
        super().__init__(name, path, acl, options)
        self.type = 'nfs'

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


class NfsShareService(ShareService):
    def __init__(self):
        self._exportFiles = ['/etc/exports']
        self._reloadCMD = 'exportfs -arv'
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
                            options={servername: options}
                        )
                    else:
                        share = shares[name]
                        for s in ro:
                            share.acl.read.append(s)
                        for s in rw:
                            share.acl.write.append(s)
                        share.options[servername, options]
                    shares[name] = share
        return shares