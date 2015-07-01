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

from functional.common import test

BASIC_LIST_HEADERS = ['ID', 'Name']


class FlavorTests(test.TestCase):

    flavor_fields = ['id', 'name', 'ram', 'disk']

    def _create_dummy_flavor(self):
        flavor_name = data_utils.rand_name('TestFlavor')
        raw_output = self.openstack(
            'flavor create '
            '--ram 512 '
            '--disk 10 '
            '--swap 2 '
            '%s' % flavor_name)
        items = self.parse_show(raw_output)
        self.assert_show_structure(items, self.flavor_fields)
        self.addCleanup(self.openstack,
                        'flavor delete %s' % flavor_name)
        return flavor_name

    @classmethod
    def setUpClass(cls):
        cls.flavor_name = data_utils.rand_name('TestFlavor')
        cls.openstack(
            'flavor create '
            '--ram 512 '
            '--disk 10 '
            '--swap 2 '
            '%s' % cls.flavor_name)

    @classmethod
    def tearDownClass(cls):
        cls.openstack(
            'flavor delete %s' % cls.flavor_name)

    def test_flavor_list(self):
        raw_output = self.openstack('flavor list')
        items = self.parse_listing(raw_output)
        self.assert_table_structure(items, BASIC_LIST_HEADERS)

    def test_flavor_show(self):
        raw_output = self.openstack('flavor show %s' % self.flavor_name)
        flavor = self.parse_show_as_object(raw_output)
        self.assert_show_structure(flavor, self.flavor_fields)

    def test_flavor_set(self):
        flavor_name = self._create_dummy_flavor()
        raw_output = self.openstack(
            'flavor set '
            '--property k1=v1 '
            '--property k2=v2 '
            '%s' % flavor_name)
        flavor = self.parse_show_as_object(raw_output)
        self.assertEqual("k1='v1', k2='v2'", flavor['properties'])

    def test_flavor_unset(self):
        flavor_name = self._create_dummy_flavor()
        raw_output = self.openstack(
            'flavor set '
            '--property k1=v1 '
            '--property k2=v2 '
            '%s' % flavor_name)
        flavor = self.parse_show_as_object(raw_output)
        self.assertEqual("k1='v1', k2='v2'", flavor['properties'])
        raw_output = self.openstack(
            'flavor unset '
            '--property k1 '
            '--property k2 '
            '%s' % flavor_name)
        flavor = self.parse_show_as_object(raw_output)
        self.assertEqual('', flavor['properties'])

    def test_flavor_create(self):
        flavor_name = data_utils.rand_name('TestFlavor')
        raw_output = self.openstack(
            'flavor create '
            '--ram 512 '
            '--disk 10 '
            '--swap 2 '
            '--vcpus 2 '
            '%s' % flavor_name)
        items = self.parse_show(raw_output)
        self.assert_show_structure(items, self.flavor_fields)
        self.addCleanup(self.openstack,
                        'flavor delete %s' % flavor_name)

    def test_flavor_delete(self):
        flavor_name = data_utils.rand_name('TestFlavor')
        raw_output = self.openstack(
            'flavor create '
            '--ram 512 '
            '--disk 10 '
            '--swap 2 '
            '--vcpus 2 '
            '%s' % flavor_name)
        items = self.parse_show(raw_output)
        self.assert_show_structure(items, self.flavor_fields)
        raw_output = self.openstack('flavor delete %s' % flavor_name)
        self.assertEqual(0, len(raw_output))
