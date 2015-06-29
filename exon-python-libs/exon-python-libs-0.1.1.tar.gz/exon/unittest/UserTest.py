__author__ = 'Stephan Conrad <stephan@conrad.pics>'

import unittest
from exon.utils.samba.usersandgroup import UsersAndGroup, SAMBAUserException, SambaUserNotFound

class UserAndGroupTest(unittest.TestCase):
#class UserAndGroupTest(object):

    def setUp(self):
        self.users = UsersAndGroup()
        self.userMap = {
            'sAMAccountName': 'unitTest',
            'groups' : ['Domain Users', 'Domain Admins'],
            'unix_user': True,
            'password': 'test-1234',
            'givenName': 'Unit',
            'sn': 'Test'
        }

    def tearDown(self):
        self.users.deleteUser('unitTest')

    def _createUser(self):
        return self.users.createOrModifyUser(self.userMap)

    def test_UserCreate(self):
        userMap = {
            'sAMAccountName': 'unitTest',
            'groups' : ['Domain Users', 'Domain Admins'],
            'unix_user': True,
            'password': 'test-1234'
        }
        self.assertRaises(SAMBAUserException, self.users.createOrModifyUser, userMap)
        userMap['givenName'] = 'Unit'
        userMap['sn'] = 'Test'
        user = self.users.createOrModifyUser(userMap)
        self.assertIsInstance(user, dict)
        self.assertEqual(user['unix_user']['unixHomeDirectory'], '/home/unitTest')
        self.assertEqual(user['unix_user']['loginShell'], '/bin/bash')
        self.assertIsInstance(self.users.getUserByAccount('unitTest'), dict)
        self.assertIn('Domain Users', user['groups'])
        self.users.deleteUser('unitTest')
        self.assertRaises(SAMBAUserException, self.users.getUserByAccount, 'unitTest')

    def test_UserModify(self):
        user = self.users.createOrModifyUser(self.userMap)
        self.assertIsInstance(user, dict)
        self.assertEqual(user['unix_user']['unixHomeDirectory'], '/home/unitTest')
        self.assertEqual(user['unix_user']['loginShell'], '/bin/bash')
        self.assertIsInstance(self.users.getUserByAccount('unitTest'), dict)
        userMap = self.userMap
        userMap['unix_user'] = False
        user = self.users.createOrModifyUser(userMap)
        self.assertFalse(user['unix_user'])
        self.users.deleteUser('unitTest')
        self.assertRaises(SAMBAUserException, self.users.getUserByAccount, 'unitTest')

    def test_GroupCreate(self):
        self.users.createOrModifyGroup('unitTestGroup', True, [])
        self.assertTrue(self.users.groupExists('unitTestGroup'))
        self.users.deleteGroup('unitTestGroup')
        self.assertFalse(self.users.groupExists('unitTestGroup'))

    def test_GroupModify(self):
        self.users.createOrModifyGroup('unitTestGroup', True, [])
        self.assertTrue(self.users.groupExists('unitTestGroup'))
        user = self._createUser()
        group = self.users.createOrModifyGroup('unitTestGroup', False, [user['name']])
        self.assertIn(user['name'],group['users'])
        self.assertFalse(group['unix_user'])
        self.users.deleteGroup('unitTestGroup')
        self.assertFalse(self.users.groupExists('unitTestGroup'))


if __name__ == '__main__':
    users = UsersAndGroup()
    userMap = {
        'sAMAccountName': 'unitTest',
        'groups' : ['Domain Users', 'Domain Admins'],
        'unix_user': True,
        'password': 'test-1234'
    }
    userMap['givenName'] = 'Unit'
    userMap['sn'] = 'Test'
    user = users.createOrModifyUser(userMap)
    print(type(user))