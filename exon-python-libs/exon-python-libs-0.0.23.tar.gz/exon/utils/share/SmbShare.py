__author__ = 'Stephan Conrad <stephan@conrad.pics>'

from os.path import isfile, join
import shutil
from exon.utils.share import ShareService, Share, Acl
from exon.utils.command.execute import exec as run
from configparser import ConfigParser, RawConfigParser
import re

class SmbAcl(Acl):
    """
    Extended Acl class for AFP special right management
    """
    def __init__(self,read = [], write = [], valid = [], invalid = []):
        super().__init__(read, write)
        self.valid = valid
        self.invalid = invalid

    def __repr__(self):
        return '{valid users: %s, invalid users: %s}' %(self.valid, self.invalid)

class SmbShare(Share):


    def __init__(self, name=None, path=None, acl=SmbAcl(), options={}):
        super().__init__(name, path, acl, options)

    def toJson(self):
        ret = {
            'valid_users': [],
            'valid_groups': [],
            'invalid_users': [],
            'invalid_groups': [],
            'read_users': [],
            'read_groups': [],
            'write_users': [],
            'write_groups': [],
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
        for value in self.acl.write:
            if value.startswith('@'):
                ret['write_groups'].append(''.join(value[1:]))
            else:
                ret['write_users'].append(value)
        for value in self.acl.read:
            if value.startswith('@'):
                ret['read_groups'].append(''.join(value[1:]))
            else:
                ret['read_users'].append(value)
        return ret

    @classmethod
    def fromJson(cls, map):
        share = cls()
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

        read = map['read_users']
        for group in map['read_groups']:
            if ' ' in group:
                group = '"%s"' % group
            read.append('@%s' % group)
        write = map['write_users']
        for group in map['write_groups']:
            if ' ' in group:
                group = '"%s"' % group
            write.append('@%s' % group)
        share.acl.read = read
        share.acl.write = write
        share.acl.valid = valid
        share.acl.invalid = invalid
        return share


class SmbShareService(ShareService):
    def __init__(self):
        self._configFile = '/etc/samba/smb.conf'
        self._reloadCmd = 'smbcontrol smbd reload-config'
        self._testCmd = 'testparm -s'
        self.config = RawConfigParser()
        self.config.read(self._configFile)

    def fromJson(self, map):
        return SmbShare.fromJson(map)

    def getShares(self):
        shares = {}
        for section in self.config.sections():
            if section != 'global':
                share = SmbShare(name=section)
                for key in self.config[section]:
                    if key == 'path':
                        share.path = self.config[section][key]
                    elif key == 'read list':
                        share.acl.read = re.split('\s+', self.config[section][key])
                    elif key == 'write list':
                        share.acl.write = re.split('\s+', self.config[section][key])
                    elif key == 'invalid users':
                        share.acl.invalid = re.split('\s+', self.config[section][key])
                    elif key == 'valid users':
                        share.acl.valid = re.split('\s+', self.config[section][key])
                    else:
                        share.options[key] = self.config[section][key]
                shares[section] = share
        return shares

    def delete(self, name):
        self.config.remove_section(name)
        with open(self._file, 'w') as file:
            self.config.write(file)
        return self._reload()

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
            if len(share.acl.write) >= 1:
                self.config[name]['write list'] = ' '.join(share.acl.valid)
            if len(share.acl.read) >= 1:
                self.config[name]['read list'] = ' '.join(share.acl.invalid)
            if 'writable' not in share.options:
                self.config[name]['writable']= 'yes'
            if 'read only' not in share.options:
                self.config[name]['read only']= 'no'

        else:
            self.config.add_section(name)
            self.config[name]['path'] = share.path
            if len(share.acl.valid) >= 1:
                self.config[name]['valid users'] = ' '.join(share.acl.valid)
            if len(share.acl.invalid) >= 1:
                self.config[name]['invalid users'] = ' '.join(share.acl.invalid)
            if len(share.acl.write) >= 1:
                self.config[name]['write list'] = ' '.join(share.acl.valid)
            if len(share.acl.read) >= 1:
                self.config[name]['read list'] = ' '.join(share.acl.invalid)
            if 'writable' not in share.options:
                self.config[name]['writable']= 'yes'
            if 'read only' not in share.options:
                self.config[name]['read only']= 'no'

        return self._reload()

    def _reload(self):
        shutil.copy(self._configFile, '%s.bak'% self._configFile)
        with open(self._configFile, 'w') as file:
            self.config.write(file)
        out = run(self._testCmd)
        if out.rc != 0:
            shutil.copy('%s.bak'% self._configFile, self._configFile)
            return False
        out = run(self._reloadCmd)
        return bool(out.rc == 0)