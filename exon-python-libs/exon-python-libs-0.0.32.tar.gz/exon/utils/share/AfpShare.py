__author__ = 'Stephan Conrad <stephan@conrad.pics>'
from os import listdir
from os.path import isfile, join
from exon.utils.share import ShareService, Share, Acl
from exon.utils.systemd import Units
from configparser import ConfigParser
import re

class AfpAcl(Acl):
    """
    Extended Acl class for AFP special right management
    """
    def __init__(self, valid = [], invalid = []):
        super().__init__(None, None)
        self.valid = valid
        self.invalid = invalid

    def __repr__(self):
        return '{valid users: %s, invalid users: %s}' %(self.valid, self.invalid)


class AfpShare(Share):
    """
    Extended Share class for AFP Shares
    """
    def __init__(self, name=None, path=None, acl=AfpAcl(), options={}):
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

    @classmethod
    def fromJson(cls, map):
        share = cls(acl = AfpAcl())
        valid = map['valid_users']
        for group in map['valid_groups']:
            if ' ' in group:
                group = '"%s"' % group
            valid.append('@%s' % group)
        invalid = map['invalid_users']
        for group in map['invalid_groups']:
            if ' ' in group:
                group = '"%s"' % group
            valid.append('@%s' % group)
        share.acl.valid = valid
        share.acl.invalid = invalid
        return share


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



    def writeShare(self, share):
        name = share.name
        if name in self.config.sections():
            for key in self.config[name]:
                if key == 'basedir regex' or key == 'path':
                    oldPath = self.config[name][key]
                    if oldPath != share.path:
                        self.config[name][key] = share.path
            if len(share.acl.valid) >= 1:
                self.config[name]['valid users'] = ' '.join(share.acl.valid)
            if len(share.acl.invalid) >= 1:
                self.config[name]['invalid users'] = ' '.join(share.acl.invalid)

        else:
            self.config.add_section(name)
            self.config[name]['path'] = share.path
            if len(share.acl.valid) >= 1:
                self.config[name]['valid users'] = ' '.join(share.acl.valid)
            if len(share.acl.invalid) >= 1:
                self.config[name]['invalid users'] = ' '.join(share.acl.invalid)
        with open(self._file, 'w') as file:
            self.config.write(file)
        return Units.restart('netatalk.service ')

    def fromJson(self, map):
        return AfpShare.fromJson(map)

    def delete(self, name):
        self.config.remove_section(name)
        with open(self._file, 'w') as file:
            self.config.write(file)
        return Units.restart('netatalk.service ')


