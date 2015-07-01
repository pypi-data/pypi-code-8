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

from openstack.tests.unit import test_proxy_base

from helionsdk.dns.v1 import _proxy
from helionsdk.dns.v1 import domain


class TestDnsProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestDnsProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_domain_delete(self):
        self.verify_delete2(domain.Domain,
                            self.proxy.delete_domain, False)

    def test_domain_delete_ignore(self):
        self.verify_delete2(domain.Domain,
                            self.proxy.delete_domain, True)

    def test_domain_find(self):
        self.verify_find('helionsdk.dns.v1.domain.Domain.find',
                         self.proxy.find_domain)

    def test_domain_get(self):
        self.verify_get2('openstack.proxy.BaseProxy._get',
                         self.proxy.get_domain,
                         method_args=["resource_or_id"],
                         expected_args=[domain.Domain, "resource_or_id"])

    def test_domains(self):
        self.verify_list2(self.proxy.domains,
                          expected_args=[domain.Domain],
                          expected_kwargs={})

    def test_domain_update(self):
        kwargs = {"x": 1, "y": 2, "z": 3}
        self.verify_update2('openstack.proxy.BaseProxy._update',
                            self.proxy.update_domain,
                            method_args=["resource_or_id"],
                            method_kwargs=kwargs,
                            expected_args=[domain.Domain,
                                           "resource_or_id"],
                            expected_kwargs=kwargs)
