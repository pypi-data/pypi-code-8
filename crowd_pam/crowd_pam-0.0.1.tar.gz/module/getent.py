"""
Copyright @ 2015 Atlassian Pty Ltd

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import sys
import pwd
import grp
from logs import get_logger as logger


class GetEnt:
    """
        class GetEnt:
            This class performs management operations
            for the local user accounts.
    """

    def __init__(self, log=logger("DEBUG")):
        self.log = log

    def __safeSystemCall(self, cmd):
        return os.system(cmd) == 0

    def doesUserExist(self, userName):
        """
            GetEnt::doesUserExist()
                This method returns a boolean result based on whether or not
                a given username exists.
        """
        try:
            pwd.getpwnam(userName)
            self.log.info('user exists ({})'.format(userName))
            return True
        except KeyError:
            self.log.info('user does not exist ({})'.format(userName))
            return False

    def doesGroupExist(self, groupName):
        """
            GetEnt::doesGroupExist()
                This method returns a boolean result based on whether or not
                a given groupname exists.
        """
        try:
            grp.getgrnam(groupName)
            self.log.debug('group exists ({})'.format(groupName))
            return True
        except KeyError:
            self.log.debug('group exists ({})'.format(groupName))
            return False

    def createUser(self, userName):
        """
            GetEnt::createUser()
                This method will create a local Linux user in /etc/passwd
                with disabled password.
        """
        self.log.debug("crowd_pam:getent::createUser() starting")
        if not self.doesUserExist(userName):
            self.log.debug("crowd_pam::getent::createUser() no user exists.")
            args = [
                '-p 2!2E3O!Np!B9!Mc',
                '--comment crowd-user-{}'.format(userName),
                '--shell /bin/sh',
                '--create-home'
            ]
            cmd = "useradd {} {}".format(' '.join(args), userName)
            self.__safeSystemCall(cmd)
            self.log.info('crowd_pam::getent: created user {}'.format(userName))
        return True

    def createGroup(self, groupName, gid=None):
        """
            GetEnt::createGroup()
                This method will create a local user group.
        """
        if not self.doesGroupExist(groupName):
            args = []
            if gid is not None:
                args.append('--gid {}'.format(gid))
            self.__safeSystemCall("groupadd {} {}".format(' '.join(args), groupName))
            self.log.info('crowd_pam created group {}'.format(groupName))
        return True

    def __serializeGroupList(self, groups):
        if type(groups) is str:
            return groups
        elif type(groups) is list:
            if len(groups) == 0:
                # assume we want to remove from all groups.
                return None
            else:
                return ','.join(groups)
        else:
            raise Exception("Unhandle-able type in GetEnt::__serializeGroupList()")

    def addGroup(self, group):
        cmd = "groupadd -f {}".format(group)
        self.__safeSystemCall(cmd)
        self.log.info("group added: {}".format(group))
        return True

    def addUserToGroup(self, userName, groups):
        """
            GetEnt::addUserToGroup():
                This method will add a given user to a given group.
        """
        groupList = self.__serializeGroupList(groups)
        if groupList is None:
            return True

        for group in groupList.split(","):
            self.addGroup(group)

        if not self.doesUserExist(userName):
            self.createUser(userName)
        cmd = "usermod --groups {} {}".format(groupList, userName)
        self.__safeSystemCall(cmd)
        self.log.info('crowd_pam added user {} to group(s) {}'.format(userName, groupList))
        return True

if __name__ == "__main__":
    existingUser = 'root'
    existingGroup = 'sys'
    nonExistingUser = 'foobarUser'
    nonExistingGroup = 'foobarGroup'
    testUser = 'testUser'
    testGroup = 'testGroup'
    otherGroup = 'otherGroup'

    try:
        c = GetEnt()
        if c.doesUserExist(nonExistingUser):
            print "Fail: doesUserExist detected a non-existing user."
            sys.exit(1)
        else:
            print "Pass: doesUserExist passes test of non-existent user"
        if c.doesUserExist(existingUser):
            print "Pass: doesUserExist passes test of existing user"
        else:
            print "Fail: doesUserExist fails test of existing user"
            sys.exit(1)
        if c.doesGroupExist(nonExistingGroup):
            print "Fail: doesGroupExist detected a non-existing group"
            sys.exit(1)
        else:
            print "Pass: doesGroupExist did not detect non-existing group."

        if c.createGroup(testGroup) and c.doesGroupExist(testGroup):
            print "Pass: createGroup worked."
        else:
            print "Fail: createGroup failed to create testGroup"
            sys.exit(1)

        if c.createUser(testUser) and c.doesGroupExist(testGroup) and c.doesUserExist(testUser):
            print "Pass: Created user and user's group"
        else:
            print "Fail: createUser failed to create user and/or user's group"
            sys.exit(1)

        if c.addUserToGroup(testUser, otherGroup):
            print "Pass: addUserToGroup added user to group"
        else:
            print "Fail: addUserToGroup did not add user to group"
            sys.exit(1)
    except Exception as e:
        print "Fail: An Exception Occurred: {}".format(e)
        sys.exit(1)
    print "PASS: All Tests Pass"
    sys.exit(0)
