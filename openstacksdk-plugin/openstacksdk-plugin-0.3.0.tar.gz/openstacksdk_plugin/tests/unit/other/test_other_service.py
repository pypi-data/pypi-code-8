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

from openstacksdk_plugin.other import other_service


class TestOtherService(testtools.TestCase):

    def test_service(self):
        sut = other_service.OtherService()
        self.assertEqual('vendor', sut.vendor)
        self.assertEqual('other', sut.service_type)
        self.assertEqual('public', sut.visibility)
        self.assertIsNone(sut.region)
        self.assertIsNone(sut.service_name)
        self.assertEqual(1, len(sut.valid_versions))
        self.assertEqual('v1', sut.valid_versions[0].module)
        self.assertEqual('v1', sut.valid_versions[0].path)
