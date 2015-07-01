# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import testtools

from helionsdk.dns import version

IDENTIFIER = 'v2.0'
EXAMPLE = {
    'id': IDENTIFIER,
    'links': '2',
    'status': '3',
}


class TestVersion(testtools.TestCase):

    def test_basic(self):
        sut = version.Version()
        self.assertEqual('version', sut.resource_key)
        self.assertEqual('versions', sut.resources_key)
        self.assertEqual('/', sut.base_path)
        self.assertEqual('dns', sut.service.service_type)
        self.assertFalse(sut.allow_create)
        self.assertFalse(sut.allow_retrieve)
        self.assertFalse(sut.allow_update)
        self.assertFalse(sut.allow_delete)
        self.assertTrue(sut.allow_list)

    def test_make_it(self):
        sut = version.Version(EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sut.id)
        self.assertEqual(EXAMPLE['links'], sut.links)
        self.assertEqual(EXAMPLE['status'], sut.status)
