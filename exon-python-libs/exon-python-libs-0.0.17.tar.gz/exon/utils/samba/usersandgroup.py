__author__ = 'Stephan Conrad <stephan@conrad.pics>'

from os import path, environ
from exon.utils.command.execute import exec as run
from exon.utils.ldap.parseRecord import parseRecord
from exon.utils.ldap.samba import runLdapQuery
import memcache
import configparser
from exon.utils.fileutils import readfileAsArray

LDB_SAM_FILE='/var/lib/samba/private/sam.ldb'
SAMBA_LDB_PATHS='/usr/lib/samba/ldb'

# Group ID's: ldbsearch -H /var/lib/samba/private/sam.ldb '(&(objectCategory=group)(sAMAccountName=Domain Users))' primarygrouptoken
# Supported Shells /1.0/installedShells

class SAMBAUserException(Exception):
    pass

class SambaUserNotFound(SAMBAUserException):
    pass

class UsersAndGroup(object):
    """
    This class handles the Samba user and group
    """

    _NEEDED_FIELDS = ('dn', 'sAMAccountName', 'givenName', 'sn', 'displayName', 'primaryGroupID')
    _ARRAY_FIELDS = ('memberOf')
    _IGNORE_KEYS = ('sAMAccountType', 'systemUser')
    _UNIX_KEYS = ('uidNumber', 'loginShell', 'unixHomeDirectory', 'gidNumber')

    def __init__(self):
        LDB_MODULES_PATH = []
        if "LDB_MODULES_PATH" in environ:
            LDB_MODULES_PATH = environ.get("LDB_MODULES_PATH").split(":")
        if SAMBA_LDB_PATHS not in LDB_MODULES_PATH:
            LDB_MODULES_PATH.append(SAMBA_LDB_PATHS)
        environ["LDB_MODULES_PATH"] = ":".join(LDB_MODULES_PATH)
        if path.exists(LDB_SAM_FILE):
            self._ldbSamFile = LDB_SAM_FILE
        else:
            raise SAMBAUserException("sam ldb database %s not found" % LDB_SAM_FILE)
        self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        config = configparser.ConfigParser()
        config.read('/etc/samba/smb.conf')
        self.domain = config['global']['workgroup'].lower()

    def listUsers(self):
        """
        Returns a list of all Users with username and diplayname
        :return:
        """
        out = runLdapQuery(self._ldbSamFile, '(objectClass=person)', ["sAMAccountName", "displayName", "isCriticalSystemObject", "sAMAccountType"])
        if type(out) != list:
            raise SAMBAUserException("can not query users. STDOUT: %s STDERR: %s" % (out.stdout, out.stderr))
        return parseRecord(out)

    def getUserByAccount(self, name):
        """
        Returns the details of a user
        :param name: the user name
        :return:
        """
        out = runLdapQuery(self._ldbSamFile, '(&(objectClass=person)(sAMAccountName=%s))' % name, [
                "dn",
                "sAMAccountName",
                "givenName",
                "sn",
                "sAMAccountType",
                "displayName",
                "primaryGroupID",
                "uidNumber",
                "loginShell",
                "unixHomeDirectory",
                "gidNumber",
                "memberOf"
            ])
        if type(out) != list:
            raise SAMBAUserException("can not query user. STDOUT: %s STDERR: %s" % (out.stdout, out.stderr))
        parse = parseRecord(out)
        if len(parse) > 1:
            raise SAMBAUserException("more than one user with userid %s found" % name)
        elif len(parse) == 0:
            raise SambaUserNotFound("no user with id %s found" % name)
        u = parse[0]
        user = {}
        unix = False
        if 'uidNumber' in u:
            unix = True
            user["unix_user"] = {}
        else:
            user["unix_user"] = False
        for key in u:
            if key not in self._IGNORE_KEYS:
                if key in self._UNIX_KEYS:
                    if unix:
                        user["unix_user"][key] = u[key]
                elif key == "primaryGroupID":
                    g = self.getGroupById(u["primaryGroupID"])
                    if "groups" not in user:
                        user["groups"] = [g]
                    elif type(user["groups"]) == list:
                        user["groups"].appand(g)
                    else:
                        user["groups"] = [g]
                elif key in self._ARRAY_FIELDS:
                    if key not in u:
                        user[key] = [u[key]]
                    elif type(user[key]) == list:
                        user[key].appand(u[key])
                    else:
                        user[key] = [u[key]]
                else:
                    user[key] = u[key]
        return user


    def getGroupById(self, gid):
        """
        Get the sAMAccountName for group id
        :param gid: groupid
        :return: sAMAccountName
        """
        key = "samba_gid_%s" % gid
        name = self.mc.get(key)
        if name != None:
            return name
        out = runLdapQuery(self._ldbSamFile, '(&(objectCategory=group))', ["primarygrouptoken", "sAMAccountName", "sAMAccountType"])
        if type(out) != list:
            raise SAMBAUserException("can not query groups. STDOUT: %s STDERR: %s" % (out.stdout, out.stderr))
        groups = parseRecord(lines=out, accountType='268435456')
        for g in groups:
            if 'sAMAccountName' in g and 'primaryGroupToken' in g:
                self.mc.set('samba_gid_%s' % g['primaryGroupToken'], g['sAMAccountName'])
                if g['sAMAccountName'] == "Domain Users":
                    self.mc.set('samba_domain_user_id', g['primaryGroupToken'])
        return self.mc.get(key)

    def createUser(self, userData = {}):
        if type(userData) != dict:
            raise SAMBAUserException("userDate must be a dict")
        error = False
        fields = []
        if "primaryGroupID" not in userData:
            self.getGroupById(513)
            userData['primaryGroupID'] = self.mc.get('samba_domain_user_id')
        print(userData)
        for key in self._NEEDED_FIELDS:
            if key not in userData:
                error = True
                fields.append(key)
        if error:
            raise SAMBAUserException("userData misses following keys: %s" % ", ".join(fields))
        pass

    def getNextUid(self):
        """
        Returns the next higher uid
        :return: uid
        """
        return self._findLastUid() + 1

    def _findLastUid(self):
        """
        Returns the hiest uid in the ldap
        """
        out = runLdapQuery(self._ldbSamFile, '(&(objectClass=person)(uidNumber=*))', ["uidNumber"])
        if type(out) != list:
            raise SAMBAUserException("Error finding last uid. RC: %s STDOUT: %s STDERR %s" %(
                str(out.rc),
                out.stdout,
                out.stderr
            ))
        p = parseRecord(out, False)
        uid = 1000
        for e in p:
            if "uidNumber" in e:
                id = int(e["uidNumber"])
                if id > uid:
                    uid = id
        return uid

def getAllInstalledShells():
    """
    Retruns a list of all installed Shells
    :return:
    """
    ret = []
    for line in readfileAsArray('/etc/shells'):
        if line.startswith('/'):
            ret.append(line)
    return ret

if __name__ == '__main__':
    u = UsersAndGroup()
    print(u.getUserByAccount("stephan"))
    print(u.getGroupById(513))
    print("============================")
    print(u.createUser())