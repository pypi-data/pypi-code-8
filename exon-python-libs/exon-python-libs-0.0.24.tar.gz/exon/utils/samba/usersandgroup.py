__author__ = 'Stephan Conrad <stephan@conrad.pics>'

from os import path, environ
from exon.utils.command.execute import exec as run
from exon.utils.ldap.parseRecord import parseRecord
from exon.utils.ldap.samba import runLdapQuery, modifyLdap, getLdifByDn
import memcache
import configparser
from exon.utils.fileutils import readfileAsArray
from exon.utils.samba import ParseAdGroupType
import logging

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

    _NEEDED_FIELDS = ('sAMAccountName', 'givenName', 'sn', 'primaryGroupID')
    _ARRAY_FIELDS = ('memberOf')
    _IGNORE_KEYS = ('sAMAccountType', 'systemUser')
    _UNIX_KEYS = ('uidNumber', 'loginShell', 'unixHomeDirectory', 'gidNumber')

    _IGNORE_GROUPS = (
        'Enterprise Read-Only Domain Controllers',
        'Read-Only Domain Controllers',
        'Group Policy Creator Owners',
        'Domain Controllers',
        'Enterprise Admins',
        'Domain Computers',
        'DnsUpdateProxy',
        'Schema Admins',
    )

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

    def getUserByAccount(self, name, plainLdif = False):
        """
        Returns the details of a user
        :param name: the user name
        :return:
        """
        filter = [
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
                "memberOf",
                'msSFU30NisDomain',
                'msSFU30Name'
            ]
        out = runLdapQuery(self._ldbSamFile, '(&(objectClass=person)(sAMAccountName=%s))' % name, filter)
        if type(out) != list:
            raise SAMBAUserException("can not query user. STDOUT: %s STDERR: %s" % (out.stdout, out.stderr))
        parse = parseRecord(out)
        if len(parse) > 1:
            raise SAMBAUserException("more than one user with userid %s found" % name)
        elif len(parse) == 0:
            raise SambaUserNotFound("no user with id %s found" % name)
        if plainLdif:
            return parse[0]
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
                if key =='sAMAccountName':
                    user['name'] = u['sAMAccountName']
                    user['sAMAccountName'] = u['sAMAccountName']
                if key in self._UNIX_KEYS:
                    if unix:
                        user["unix_user"][key] = u[key]
                elif key == "primaryGroupID":
                    g = self.getGroupById(u["primaryGroupID"])
                    user["primaryGroupID"] = u[key]
                    if "groups" not in user:
                        user["groups"] = [g]
                    elif type(user["groups"]) == list:
                        user["groups"].appand(g)
                    else:
                        user["groups"] = [g]
                elif key in self._ARRAY_FIELDS:
                    if key not in user:
                        user[key] = u[key]
                    elif type(user[key]) != list:
                        user[key].appand(u[key])
                    else:
                        user[key] = [u[key]]
                else:
                    user[key] = u[key]
        if 'memberOf' in user:
            if type(user['memberOf']) == list:
                for dn in user['memberOf']:
                    try:
                        g = self.getObjectByDN(dn, accountType=False)
                        if 'sAMAccountName' in g:
                            name = g['sAMAccountName']
                            if name not in user['groups']:
                                user['groups'].append(name)
                    except SAMBAUserException as e:
                        logging.error(e)
            else:
                g = self.getObjectByDN(user['memberOf'], accountType=False)
                if 'sAMAccountName' in g:
                    name = g['sAMAccountName']
                    if name not in user['groups']:
                        user['groups'].append(name)
            del user['memberOf']
        return user

    def getObjectByDN(self, dn, accountType='805306368'):
        out = getLdifByDn(self._ldbSamFile, dn)
        if type(out) != list:
            raise SAMBAUserException("can not query groups. STDOUT: %s STDERR: %s" % (out['stdout'], out['stderr']))
        groups = parseRecord(lines=out, accountType=accountType)
        if len(groups) == 1:
            return groups[0]

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

    def createOrModifyUser(self, userData = {}):
        if type(userData) != dict:
            raise SAMBAUserException("userDate must be a dict")
        error = False
        fields = []
        if "primaryGroupID" not in userData:
            self.getGroupById(513)
            userData['primaryGroupID'] = self.mc.get('samba_domain_user_id')
            if 'groups' in userData:
                pGroup = self.getGroupById(userData['primaryGroupID'])
                if pGroup not in userData['groups']:
                    userData['groups'].appand(pGroup)
        if "unix_user" in userData:
            unix = userData["unix_user"]
            if type(unix) == bool:
                userData["unix_user"] = {
                    "id":self.getNextUid(),
                    "default_group":"10000",
                    "shell":"/bin/bash"
                }
            elif type(unix) == dict:
                 userData["unix_user"] = unix
        modifyUser = self.userExists(userData["sAMAccountName"])
        for key in self._NEEDED_FIELDS:
            if key not in userData:
                if modifyUser and key in ('givenName', 'sn'):
                    pass
                else:
                    error = True
                    fields.append(key)
        if "password" not in userData and not modifyUser:
            error = True
            fields.append("password")
        if error:
            raise SAMBAUserException("userData misses following keys: %s" % ", ".join(fields))
        if modifyUser:
            return self._modifyUser(userData=userData, unix=unix)
        else:
            return self._createUser(userData=userData, unix=unix)

    def _modifyUser(self, userData = {}, unix = None):
        """
        Modifies a user
        :param userData: user data object
        :param unix: unix data
        :return: user data
        """
        ldif = []
        changedKeys = []
        adData = self.getUserByAccount(userData["sAMAccountName"], plainLdif=False)
        if 'dn' in adData:
            ldif.append('dn: %s' % adData['dn'])
        else:
            raise SAMBAUserException("Data from AD do not contain dn")
        ldif.append('changetype: modify')
        changePassword = False
        for key in userData:
            if key == 'unix_user':
                createUnixUser = True
                if type(userData["unix_user"]) == bool:
                    createUnixUser = userData["unix_user"]
                else:
                    createUnixUser = unix
                isUnixUser = adData["unix_user"] != False
                deleteUnixUser = isUnixUser and not unix
                if deleteUnixUser:
                    changedKeys.append('unix')
                    ldif.append('-')
                    adplain = self.getUserByAccount(userData["sAMAccountName"], plainLdif=True)
                    for key in ('uidNumber', 'gidNumber', 'loginShell', 'unixHomeDirectory', 'msSFU30NisDomain', 'msSFU30Name', 'unixUserPassword'):
                        if key in adplain:
                            ldif.append('delete: %s' % key)
                    ldif.append('-')
                elif isUnixUser == False and createUnixUser:
                    changedKeys.append('unix')
                    if 'password' not in userData:
                        raise SAMBAUserException("Can not create unix user if no password is provided")
                    ldif.append('-')
                    ldif.append('add: uidNumber')
                    ldif.append('uidNumber: %s' % userData[key]["id"])
                    ldif.append('-')
                    ldif.append('add: gidNumber')
                    ldif.append('gidNumber: %s' % userData[key]["default_group"])
                    ldif.append('-')
                    ldif.append('add: loginShell')
                    ldif.append('loginShell: %s' % userData[key]["shell"])
                    ldif.append('-')
                    ldif.append('add: unixHomeDirectory')
                    ldif.append('unixHomeDirectory: /home/%s' % userData["sAMAccountName"])
                    ldif.append('-')
                    ldif.append('add: msSFU30NisDomain')
                    ldif.append('msSFU30NisDomain: %s' % self.domain)
                    ldif.append('-')
                    ldif.append('add: msSFU30Name')
                    ldif.append('msSFU30Name: %s' % userData["sAMAccountName"])
                    ldif.append('-')

                elif isUnixUser:
                    for u in userData[key]:
                        if u == 'default_group' and adData[key]['gidNumber'] != userData[key]['default_group']:
                            changedKeys.append('unix')
                            ldif.append('-')
                            ldif.append('replace: %s' % 'gidNumber')
                            ldif.append('%s: %s' % ('gidNumber', userData[key][u]))
                        elif u == 'shell' and adData[key]['loginShell'] != userData[key]['shell']:
                            changedKeys.append('unix')
                            ldif.append('-')
                            ldif.append('replace: %s' % 'loginShell')
                            ldif.append('%s: %s' % ('loginShell', userData[key][u]))
            elif key == 'groups':
                pass
            elif key == 'password':
                changePassword = True
            else:
                if key in adData:
                    if userData[key] != adData[key]:
                        changedKeys.append(key)
                        ldif.append('-')
                        ldif.append('replace: %s' % key)
                        ldif.append('%s: %s' % (key, userData[key]))
        if 'sn' in changedKeys or 'givenName' in changedKeys:
            ldif.append('-')
            ldif.append('replace: displayName')
            ldif.append('displayName: %s %s' % (userData['givenName'], userData['sn']))
        if len(changedKeys) >= 1:
            ret = modifyLdap(self._ldbSamFile, ldif)
            if type(ret) == dict:
                raise SAMBAUserException("Error while modify user %s. STDOUT: %s STDERR: %s LDIF: %s" % (
                    userData["sAMAccountName"],
                    ret["stdout"],
                    ret["stderr"],
                    ret['ldif']
                ))
        if 'groups' in userData:
            for g in list(set(userData['groups']) - set(adData['groups'])):
                self._addUserToGroup(group=g, user=userData["sAMAccountName"])
            for g in list(set(adData['groups']) - set(userData['groups'])):
                self._removeUserFromGroup(group=g, user=userData["sAMAccountName"])
        if changePassword:
            cmd = 'samba-tool user setpassword --filter=samaccountname=%s --newpassword="%s"' % (userData["sAMAccountName"], userData['password'])
            out = run(cmd)
            if out.rc != 0:
                raise SAMBAUserException("Error while changeing password of user %s. STDOUT: %s STDERR: %s" % (
                    userData["sAMAccountName"],
                    out.stdout,
                    out.stderr
                ))
        return self.getUserByAccount(userData["sAMAccountName"])

    def _createUser(self, userData = {}, unix = None):
        """
        Creates a new user in Active Directory
        :param userData: the User data
        :return: The user created
        """
        unix_data = ""
        if unix:
            unix_data = "--nis-domain=%s --unix-home=%s --uid-number=%s --gid-number=%s --login-shell=%s" % (
                self.domain,
                "/home/%s" % userData["sAMAccountName"],
                userData["unix_user"]["id"],
                userData["unix_user"]["default_group"],
                "/bin/bash",
            )
        cmd = "samba-tool user add %s %s --use-username-as-cn --surname=%s --given-name=%s %s" % (
            userData["sAMAccountName"],
            userData["password"],
            userData["sn"],
            userData["givenName"],
            unix_data
        )
        out = run(cmd.strip())
        if out.rc != 0:
            raise SAMBAUserException("Faild to add user: %s" % out.stderr)
        newUser = self.getUserByAccount(userData["sAMAccountName"])
        if 'groups' in userData:
            for g in userData['groups']:
                if g not in newUser['groups']:
                    self._addUserToGroup(group=g, user=userData["sAMAccountName"])
        return self.getUserByAccount(userData["sAMAccountName"])

    def _deleteObject(self, accountName, kind):
        """
        Internal implemantation of deletion of an object
        :param accountName: the account name of the object
        :param kind: the Type of the object at the moment user or group
        :return: True if done
        """
        if kind not in ('user', 'group'):
            raise SAMBAUserException('The kind of deltion must be user or group')
        out=run('samba-tool %s delete "%s"' % (kind, accountName))
        if out.rc == 0:
            return True
        return False

    def deleteUser(self, accountName):
        """
        Deletes the given user in active directory
        :param accountName: username
        :return: True if done
        """
        return self._deleteObject(accountName, 'user')

    def deleteGroup(self, accountName):
        """
        Deletes the given group in active directory
        :param accountName: group name
        :return: True if done
        """
        return self._deleteObject(accountName, 'group')

    def getNextUid(self):
        """
        Returns the next higher uid
        :return: uid
        """
        return self._findLastId('uid') + 1

    def getNextGid(self):
        """
        Returns the next higher gid
        :return: gid
        """
        return self._findLastId('gid') + 1

    def userExists(self, userName):
        """
        Returns if user exists in Active Directory
        :param userName: the user name of the user
        :return: True if exists or False
        """
        try:
            return self.getUserByAccount(userName) != None
        except SambaUserNotFound as e:
            print(e)
            return False

    def groupExists(self, groupName):
        """
        Returns if group exists in Active Directory
        :param groupName: the group name of the user
        :return: True if exists or False
        """
        try:
            return self.getGroupByAccount(groupName) != None
        except SAMBAUserException:
            return False

    def _findLastId(self, kind):
        """
        Returns the highest uid in the ldap
        :param kind: Type of the id to search. Supported UID and GID
        """
        if kind not in ('uid', 'gid'):
            raise SAMBAUserException('Only uid and gid are Supported')
        objectClass  = ''
        field = ''
        if kind == 'uid':
            objectClass = 'person'
            field = 'uidNumber'
        elif kind == 'gid':
            objectClass = 'group'
            field = 'gidNumber'
        else:
            raise SAMBAUserException("No id type %s known" % kind)
        out = runLdapQuery(self._ldbSamFile, '(&(objectClass=%s)(%s=*))' % (objectClass, field), [field])
        if type(out) != list:
            raise SAMBAUserException("Error finding last uid. RC: %s STDOUT: %s STDERR %s" %(
                str(out.rc),
                out.stdout,
                out.stderr
            ))
        p = parseRecord(out, False)
        uid = 1000
        for e in p:
            if field in e:
                id = int(e[field])
                if id > uid:
                    uid = id
        return uid

    def listGroups(self):
        """
        Lists all groups of the domain
        """
        out = runLdapQuery(self._ldbSamFile, '(&(objectCategory=group))', ["sAMAccountName", "sAMAccountType", 'name'])
        if type(out) != list:
            raise SAMBAUserException("can not query groups. STDOUT: %s STDERR: %s" % (out.stdout, out.stderr))
        groups = parseRecord(lines=out, accountType='268435456')
        ret = {}
        for group in groups:
            if group['sAMAccountName'] not in self._IGNORE_GROUPS:
                ret[group['sAMAccountName']] = group['name']
        return ret

    def getGroupByAccount(self, accountName):
        """
        Returns the details of the given group
        :param accountName: the account name of the group
        """
        out = runLdapQuery(self._ldbSamFile, '(&(objectCategory=group)(sAMAccountName=%s))' % accountName, ['dn', "sAMAccountName", "sAMAccountType", 'name', 'gidNumber'])
        if type(out) != list:
            raise SAMBAUserException("can not query groups. STDOUT: %s STDERR: %s" % (out.stdout, out.stderr))
        groups = parseRecord(lines=out, accountType='268435456')
        if len(groups) != 1:
            raise SAMBAUserException("No or more than one group with name %s found" % accountName)
        group = groups[0]
        ret = {"users": []}
        if 'gidNumber' in group:
            ret["unix_user"] = {"id": group['gidNumber']}
        else:
            ret["unix_user"] = False
        if 'sAMAccountName' in group:
            ret["name"] = group['sAMAccountName']
        if 'name' in group:
            ret['display_name'] = group['name']
        if 'dn' in group:
            ret['dn'] = group['dn']
        membersOut = run('samba-tool group listmembers "%s"' % accountName)
        if membersOut.rc != 0:
            raise SAMBAUserException('could not query members for groupt %s. STDOUT: %s STDERR: %s' % (accountName, membersOut.stdout, membersOut.stderr))
        for line in membersOut.stdout:
            line = line.strip()
            if line != '':
                ret["users"].append(line)
        return ret

    def _getKeyForDn(self, dn):
        """
        Returns all keys for an dn
        :param dn:
        :return:
        """
        ldif = getLdifByDn(self._ldbSamFile, dn)
        ret = []
        if type(ldif) == dict:
            logging.info('Errror geting ldif for %s', dn)
            logging.debug('STDOUT: %s', ldif['stdout'])
            logging.debug('STDERR: %s', ldif['stderr'])
            raise Exception("error geting ldif")
        for line in ldif:
            line = line.strip()
            if not line.startswith('#') and line != '':
                (key, val) = line.split(':', 2)
                ret.append(key)
        return ret

    def _addUserToGroup(self, group, user):
        """
        adds a user to the group
        :param group: the group name
        :param user: the user name
        """
        if self.userExists(user) and self.groupExists(group):
            out = run('samba-tool group addmembers "%s" "%s"' % (group, user))
            if out.rc != 0:
                raise SAMBAUserException('could not create group %s. STDOUT: %s STDERR: %s' % (group, out.stdout, out.stderr))

    def _removeUserFromGroup(self, group, user):
        """
        removes a user to the group
        :param group: the group name
        :param user: the user name
        """
        if self.userExists(user) and self.groupExists(group):
            out = run('samba-tool group removemembers "%s" "%s"' % (group, user))
            if out.rc != 0:
                raise SAMBAUserException('could not create group %s. STDOUT: %s STDERR: %s' % (group, out.stdout, out.stderr))

    def createOrModifyGroup(self, name, unixUser=False, members = []):
        """
        Creates or modify an existing group
        :param name: the group name
        :param unixUser: if the Group should be a unix group
        :param members: a list of users witch are group memebers
        :return: the group details
        """
        if name not in self.listGroups():
            return self._createGroup(name, unixUser, members)
        else:
            return  self._modifyGroup(name, unixUser, members)

    def _createGroup(self, name, unixUser, members):
        """
        Creates an new group in ad
        :param name: Group name
        :param unixUser: should group have unix attributes
        :param members: a list of users in the group
        :return: the group details
        """
        users = None
        if len(members) >= 1:
            for user in members:
                if self.userExists(user):
                    if users == None:
                        users = []
                    users.append(user)
        unixStr = ""
        if unixUser:
            unixStr = ' --gid-number=%s --nis-domain=%s' % (self.getNextGid(), self.domain)
        cmd = 'samba-tool group add "%s"%s' % (name, unixStr)
        out = run(cmd)
        if out.rc != 0:
            raise SAMBAUserException('could not create groupt %s. STDOUT: %s STDERR: %s' % (name, out.stdout, out.stderr))
        for user in users:
            self._addUserToGroup(name, user)
        return self.getGroupByAccount(name)

    def _modifyGroup(self, name, unixUser, members):
        """
        Modify an new group in ad
        :param name: Group name
        :param unixUser: should group have unix attributes
        :param members: a list of users in the group
        :return: the group details
        """
        existingGroup = self.getGroupByAccount(name)
        allKeys = self._getKeyForDn(existingGroup['dn'])
        ldif = []
        ldif.append('dn: %s' % existingGroup['dn'])
        ldif.append('changetype: modify')
        # Checking if unix attributes should be added or deleted
        existingUnixUser = bool(existingGroup['unix_user'])
        unixAdd = False
        unixDel = False
        if existingUnixUser != unixUser:
            if existingUnixUser and not unixUser:
                unixDel = True
            elif unixUser and not existingUnixUser:
                unixAdd = True
        if unixDel:
            deleteKeys = ('gidNumber', 'msSFU30Name', 'msSFU30NisDomain')
            for key in deleteKeys:
                if key in allKeys:
                    ldif.append('-')
                    ldif.append('delete: %s' % key)
        if unixAdd:
            ldif.append('-')
            ldif.append('add: gidNumber')
            ldif.append('gidNumber: %s' % self.getNextGid())
            ldif.append('-')
            ldif.append('add: msSFU30Name')
            ldif.append('msSFU30Name: %s' % name)
            ldif.append('-')
            ldif.append('add: msSFU30NisDomain')
            ldif.append('msSFU30NisDomain: %s' % self.domain)
        userAdd = list(set(members) - set(existingGroup['users']))
        userDel = list(set(existingGroup['users']) - set(members))
        for u in userAdd:
            self._addUserToGroup(name,u)
        for u in userDel:
            self._removeUserFromGroup(name, u)
        if len(ldif) > 2:
            ret = modifyLdap(self._ldbSamFile, ldif)
            if type(ret) == dict:
                raise SAMBAUserException('can not modify group ldap. STDOUT: % STDERR: %s' % (ret['stdout'], ret['stderr']))
        return self.getGroupByAccount(name)

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
    print(u.createOrModifyUser({
        'sAMAccountName': 'stephan',
        'groups' : ['Domain Users', 'Domain Admins'],
        'unix_user': {'loginShell': '/bin/bash', 'unixHomeDirectory': '/home/test3', 'gidNumber': '1000', 'uidNumber': '10003'}
    }))
    print(u.createOrModifyUser({
        'sAMAccountName': 'stephan',
        'groups' : ['Domain Users'],
        'unix_user': {'loginShell': '/bin/bash', 'unixHomeDirectory': '/home/test3', 'gidNumber': '1000', 'uidNumber': '10003'}
    }))
    """
    print(u.getGroupById(513))
    print("============================")
    print(u.createOrModifyUser({
        "unix_user": {'shell': '/bin/bash'},
        "sAMAccountName": "test3",
        "givenName": "User",
        "sn": "Test",
        "password": "test-1234"
    }))
    """
