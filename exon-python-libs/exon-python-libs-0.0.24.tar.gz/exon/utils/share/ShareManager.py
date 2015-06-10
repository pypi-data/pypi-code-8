__author__ = 'Stephan Conrad <stephan@conrad.pics>'


from exon.utils.share.NfsShare import NfsShareService, NfsShare
from exon.utils.share.AfpShare import AfpShareService, AfpShare, AfpAcl
from exon.utils.share.SmbShare import SmbShare, SmbShareService
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
        for key in share:
            if key in self.services:
                ret = self.services[key].writeShare(share[key])
                if not ret:
                    status = ret
        return status

    def fromJson(self, map):
        share = {}
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
        status = True
        for name in share:
            ret = self.writeShare(share[name])
            if not ret:
                status = ret
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