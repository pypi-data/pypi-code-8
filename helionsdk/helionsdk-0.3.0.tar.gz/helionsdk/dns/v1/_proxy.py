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

    def create_domain(self, **attrs):
        """Create a new domain from attributes

        :param dict attrs: Keyword arguments which will be used to create
                           a :class:`~helionsdk.domain.v1.domain.Domain`,
                           comprised of the properties on the Domain class.

        :returns: The results of domain creation
        :rtype: :class:`~helionsdk.domain.v1.domain.Domain`
        """
        return self._create(domain.Domain, **attrs)

    def delete_domain(self, value, ignore_missing=True):
        """Delete a domain

        :param value: The value can be either the ID of a domain or a
                      :class:`~helionsdk.domain.v1.domain.Domain` instance.
        :param bool ignore_missing: When set to ``False``
                    :class:`~helionsdk.exceptions.ResourceNotFound` will be
                    raised when the domain does not exist.
                    When set to ``True``, no exception will be set when
                    attempting to delete a nonexistent domain.

        :returns: ``None``
        """
        self._delete(domain.Domain, value, ignore_missing)

    def find_domain(self, name_or_id):
        """Find a single domain

        :param name_or_id: The name or ID of a domain.
        :returns: One :class:`~helionsdk.compute.v1.domain.Domain` or None
        """
        return domain.Domain.find(self.session, name_or_id)

    def get_domain(self, value):
        """Get a single domain

        :param value: The value can be the ID of a domain or a
                      :class:`~helionsdk.domain.v1.domain.Domain` instance.

        :returns: One :class:`~helionsdk.domain.v1.domain.Domain`
        :raises: :class:`~helionsdk.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        return self._get(domain.Domain, value)

    def domains(self):
        """Return a generator of domains

        :returns: A generator of domain objects
        :rtype: :class:`~helionsdk.domain.v1.domain.Domain`
        """
        return self._list(domain.Domain)

    def update_domain(self, value, **attrs):
        """Update a domain

        :param value: Either the id of a domain or a
                      :class:`~helionsdk.domain.v1.domain.Domain` instance.
        :attrs kwargs: The attributes to update on the domain represented
                       by ``value``.

        :returns: The updated domain
        :rtype: :class:`~helionsdk.domain.v1.domain.Domain`
        """
        return self._update(domain.Domain, value, **attrs)
