__author__ = 'Stephan Conrad <stephan@conrad.pics>'
from os import listdir
from os.path import isfile, join
from exon.utils.share import ShareService, Share, Acl
from configparser import ConfigParser
import re

class AfpAcl(Acl):
    def __init__(self, valid = [], invalid = []):
        super().__init__(None, None)
        self.valid = valid
        self.invalid = invalid

    def __repr__(self):
        return '{valid users: %s, invalid users: %s}' %(self.valid, self.invalid)


class AfpShare(Share):
    def __init__(self, name=None, path=None, acl=Acl, options={}):
        super().__init__(name, path, acl, options)
        self.type = 'afs'

    def toJson(self):
        ret = {
            'valid_users': [],
            'valid_groups': [],
            'invalid_users': [],
            'invalid_groups': []
        }
        for value in self.acl.valid:
            if value.startswith('@'):
                ret['valid_groups'].append(''.join(value[1:]))
            else:
                ret['valid_users'].append(value)
        for value in self.acl.invalid:
            if value.startswith('@'):
                ret['invalid_groups'].append(''.join(value[1:]))
            else:
                ret['invalid_users'].append(value)
        return ret


class AfpShareService(ShareService):
    def __init__(self):
        self._file = '/etc/afp.conf'
        self.config = ConfigParser()
        self.config.read(self._file)

    def getShares(self):
        shares = {}
        for share in self.config.sections():
            if share != 'Global':
                tmp = AfpShare(acl=AfpAcl(), name=share)
                for key in self.config[share]:
                    if key == 'basedir regex' or key == 'path':
                        tmp.path = self.config[share][key]
                    else:
                        #tmp[key] = self.config[share][key]
                        if key == 'valid users':
                            tmp.acl.valid = self.config[share][key].split(' ')
                        elif key == 'invalid users':
                            tmp.acl.invalid = self.config[share][key].split(' ')
                        else:
                            tmp.options[key] = self.config[share][key]
                    shares[tmp.name] = tmp
        return shares