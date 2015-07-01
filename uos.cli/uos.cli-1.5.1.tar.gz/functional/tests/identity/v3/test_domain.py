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

from functional.common import exceptions
from functional.tests.identity.v3.test_identity import BASIC_LIST_HEADERS
from functional.tests.identity.v3.test_identity import IdentityTests


class DomainTests(IdentityTests):

    def test_domain_create(self):
        domain_id = data_utils.rand_name('TestDomain')
        raw_output = self.openstack('domain create ' + domain_id)
        items = self.parse_show(raw_output)
        self.assert_show_fields(items, self.DOMAIN_FIELDS)
        # disable domain first before deleting it
        self.addCleanup(self.openstack, 'domain delete ' + domain_id)
        self.addCleanup(self.openstack, 'domain set --disable ' + domain_id)

    def test_domain_list(self):
        self._create_dummy_domain()
        raw_output = self.openstack('domain list')
        items = self.parse_listing(raw_output)
        self.assert_table_structure(items, BASIC_LIST_HEADERS)

    def test_domain_delete(self):
        name = self._create_dummy_domain()
        self.assertRaises(exceptions.CommandFailed,
                          self.openstack, 'domain delete ' + name)

    def test_domain_show(self):
        name = self._create_dummy_domain()
        raw_output = self.openstack('domain show ' + name)
        items = self.parse_show(raw_output)
        self.assert_show_fields(items, self.DOMAIN_FIELDS)
