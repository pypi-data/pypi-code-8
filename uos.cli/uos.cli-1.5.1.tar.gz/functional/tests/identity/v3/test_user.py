#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from tempest_lib.common.utils import data_utils

from functional.tests.identity.v3.test_identity import BASIC_LIST_HEADERS
from functional.tests.identity.v3.test_identity import IdentityTests


class UserTests(IdentityTests):

    USER_FIELDS = ['email', 'enabled', 'id', 'name', 'project_id',
                   'name', 'domain_id', 'default_project_id', 'description']

    def _create_dummy_user(self):
        username = data_utils.rand_name('TestUser')
        password = data_utils.rand_name('password')
        email = data_utils.rand_name() + '@unitedstack.com'
        description = data_utils.rand_name('description')
        raw_output = self.openstack(
            'user create '
            '--domain %(domain)s '
            '--project %(project)s '
            '--password %(password)s '
            '--email %(email)s '
            '--description %(description)s '
            '--enable '
            '%(name)s' % {'domain': self.domain_name,
                          'project': self.project_name,
                          'email': email,
                          'password': password,
                          'description': description,
                          'name': username})
        item = self.parse_show(raw_output)
        self.addCleanup(
            self.openstack,
            'user delete %s' % self.parse_show_as_object(raw_output)['id'])

        self.assert_show_fields(item, self.USER_FIELDS)
        return username

    def test_user_create(self):
        username = data_utils.rand_name('TestUser')
        password = data_utils.rand_name('password')
        email = data_utils.rand_name() + '@unitedstack.com'
        description = data_utils.rand_name('description')
        raw_output = self.openstack(
            'user create '
            '--domain %(domain)s '
            '--project %(project)s '
            '--password %(password)s '
            '--email %(email)s '
            '--description %(description)s '
            '--enable '
            '%(name)s' % {'domain': self.domain_name,
                          'project': self.project_name,
                          'email': email,
                          'password': password,
                          'description': description,
                          'name': username})
        items = self.parse_show(raw_output)
        self.assert_show_fields(items, ['domain_id',
                                        'default_project_id',
                                        'email',
                                        'id',
                                        'description',
                                        'name',
                                        'enabled'])
        self.addCleanup(self.openstack,
                        'user delete --domain %(domain)s '
                        '%(name)s' % {'domain': self.domain_name,
                                      'name': username})

    def test_user_list(self):
        raw_output = self.openstack('user list')
        items = self.parse_listing(raw_output)
        self.assert_table_structure(items, BASIC_LIST_HEADERS)

    def test_user_set(self):
        username = self._create_dummy_user()
        raw_output = self.openstack('user show '
                                    '--domain %(domain)s '
                                    '%(name)s' % {'domain': self.domain_name,
                                                  'name': username})
        user = self.parse_show_as_object(raw_output)
        new_username = data_utils.rand_name('NewTestUser')
        new_email = data_utils.rand_name() + '@unitedstack.com'
        raw_output = self.openstack('user set '
                                    '--email %(email)s '
                                    '--name %(new_name)s '
                                    '%(id)s' % {'email': new_email,
                                                'new_name': new_username,
                                                'id': user['id']})
        self.assertEqual(0, len(raw_output))
        raw_output = self.openstack('user show '
                                    '--domain %(domain)s '
                                    '%(id)s' % {'domain': self.domain_name,
                                                'id': user['id']})
        new_user = self.parse_show_as_object(raw_output)
        self.assertEqual(new_username, new_user['name'])
        self.assertEqual(new_email, new_user['email'])

    def test_user_show(self):
        username = self._create_dummy_user()
        raw_output = self.openstack('user show '
                                    '--domain %(domain)s '
                                    '%(name)s' % {'domain': self.domain_name,
                                                  'name': username})
        items = self.parse_show(raw_output)
        self.assert_show_fields(items, self.USER_FIELDS)
