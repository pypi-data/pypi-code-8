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

import uuid

from helionsdk.tests.functional import base

from helionsdk.dns.v1 import domain


class TestDomain(base.BaseFunctionalTest):

    NAME = uuid.uuid4().hex
    ID = None

    @classmethod
    def setUpClass(cls):
        super(TestDomain, cls).setUpClass()
        sut = cls.conn.dns.create_domain(name=cls.NAME)
        assert isinstance(sut, domain.Domain)
        cls.assertIs(cls.NAME, sut.name)
        cls.ID = sut.id

    @classmethod
    def tearDownClass(cls):
        sut = cls.conn.dns.delete_domain(cls.NAME)
        cls.assertIs(None, sut)

    def test_find(self):
        sut = self.conn.dns.find_domain(self.NAME)
        self.assertEqual(self.ID, sut.id)

    def test_get(self):
        sut = self.conn.dns.get_domain(self.ID)
        self.assertEqual(self.NAME, sut.name)
        self.assertEqual(self.ID, sut.id)

    def test_list(self):
        names = [o.name for o in self.conn.dns.domains()]
        self.assertIn(self.NAME, names)
