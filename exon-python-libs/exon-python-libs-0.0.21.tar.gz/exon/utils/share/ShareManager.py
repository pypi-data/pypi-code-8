__author__ = 'Stephan Conrad <stephan@conrad.pics>'


from exon.utils.share.NfsShare import NfsShareService
from exon.utils.share.AfpShare import AfpShareService

class ShareManager(object):
    """
    Class for managing Shares
    """

    _SUPPORTED_SERVERS = {
        'nfs': NfsShareService,
        'afp': AfpShareService
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

if __name__ == '__main__':
    s = ShareManager()
    print(s.getShare('Homes'))