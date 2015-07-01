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

from openstack import proxy

from helionsdk.dns.v1 import domain


class Proxy(proxy.BaseProxy):

    # TODO(thowe): Convert these to new format
    def create_domain(self, **data):
        return domain.Domain(data).create(self.session)

    def delete_domain(self, **data):
        domain.Domain(data).delete(self.session)

    def find_domain(self, name_or_id):
        return domain.Domain.find(self.session, name_or_id)

    def get_domain(self, **data):
        return domain.Domain(data).get(self.session)

    def list_domains(self):
        return domain.Domain.list(self.session)

    def update_domain(self, **data):
        return domain.Domain(data).update(self.session)
