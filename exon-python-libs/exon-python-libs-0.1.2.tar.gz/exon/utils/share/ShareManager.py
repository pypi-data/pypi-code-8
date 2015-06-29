__author__ = 'Stephan Conrad <stephan@conrad.pics>'


from exon.utils.share.NfsShare import NfsShareService, NfsShare
from exon.utils.share.AfpShare import AfpShareService, AfpShare, AfpAcl
from exon.utils.share.SmbShare import SmbShare, SmbShareService
import os

class ShareManager(object):
    """
    Class for managing Shares
    """

    _SUPPORTED_SERVERS = {
        'nfs': NfsShareService,
        'afp': AfpShareService,
        'smb': SmbShareService
    }

    def __init__(self):
        self.shares = {}
        self.services = {}
        for key in ShareManager._SUPPORTED_SERVERS:
            self.services[key] = ShareManager._SUPPORTED_SERVERS[key]()

    def listShares(self):
        self.shares = {}
        for key in self.services:
            s = self.services[key].getShares()
            for share in s:
                if share not in self.shares:
                    self.shares[share] = {}
                self.shares[share][key] = s[share]
        return self.shares

    def getShare(self, name):
        if len(self.shares) == 0:
            self.listShares()
        if name not in self.shares:
            return None
        return self.shares[name]

    def writeShare(self, share):
        status = True
        name = None
        for key in share:
            name = share[key].name
            if key in self.services:
                ret = self.services[key].writeShare(share[key])
                if not ret:
                    status = ret
        self.listShares()
        tmp = self.getShare(name)
        for key in share:
            if key not in tmp:
                status = False
        return status

    def fromJson(self, map):
        share = {}
        shareTypes = {}
        for name in map:
            path = ''
            if name not in share:
                share[name] = {}
            for key in map[name]:
                if key == 'path':
                    path = map[name][key]
            for key in map[name]:
                if key in self.services:
                    share[name][key] = self.services[key].fromJson(map[name][key])
                    share[name][key].name = name
                    share[name][key].path = path
        status = []
        if not os.path.exists(path):
            os.makedirs(path)
        for name in share:
            shareTypes[name] = []
            ret = self.writeShare(share[name])
            for key in share[name]:
                shareTypes[name].append(key)
                status.append('%s => %s' %(key, ret))
        shares = self.listShares()
        status = True
        for name in share:
            for key in shareTypes[name]:
                if key not in shares[name]:
                    self.writeShare(share[name])
        shares = self.listShares()
        for name in share:
            if name in shares:
                for key in share[name]:
                    if key not in shares[name]:
                        status = False
            else:
                status = False
        return status

    def delete(self, name):
        shares = self.listShares()
        status = True
        if name in shares:
            for service in shares[name]:
                if service in self.services:
                    if not self.services[service].delete(name):
                        status = False
        return status

if __name__ == '__main__':
    import copy
    s = ShareManager()
    print(s.listShares())

    # print(s.fromJson(
    #     {"Media": {"nfs": {"write_hosts": ["localhost", "192.168.1.1"], "read_hosts": ["192.168.106.0/24"]},"afp": {"valid_users": ["stephan"], "invalid_groups": [], "invalid_users": [], "valid_groups": []}, "path": "/media"}}
    # )
    # )