#!/usr/bin/env python

"""
Copyright 2015 Violin Memory, Inc..

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import vmemclient
from vmemclient.core import restobject
from vmemclient.core.error import *


class UtilityManager01(restobject.SessionNamespace):
    _PREFIX = 'Managed by OpenStack '
    _REGISTRATION_OPERATING_SYSTEM = 'LinuxZen'
    _REGISTRATION_IP = '100.200.300.400'

    def set_managed_by_openstack_version(self, openstack_version):
        """Flag this Concerto as managed by OpenStack.

        On this version, the flag is handled by creating an otherwise
        invalid FC client with a specially formatted name:

            Managed by OpenStack (xxx) with vmemclient (yyy)

        Any clients found with this specific format, but whose OpenStack and
        vmemclient versions do not match will be removed.  If the name is not
        found, then a client with the specified name will be created.  The
        return value for this function is the results of registering the
        specified OpenStack version with Concerto.

        Arguments:
            openstack_version -- string

        Raises:
            QueryError

        """
        # Variables
        found_registration = False
        registration_value = '{0}({1}) with vmemclient ({2})'.format(
                self._PREFIX, openstack_version, vmemclient.__version__)

        # Raises: QueryError
        clients = self.parent.client.get_clients()

        # Check and see if there is already a registration
        for info in clients:
            if info['name'].startswith(self._PREFIX):
                if info['name'] == registration_value:
                    # Registration found and is valid
                    found_registration = True
                else:
                    # Registration found to be outdated; remove it
                    result = self.parent.client.delete_client(
                            object_id=info['object_id'])
                    if not result['success']:
                        self.parent.basic.log(
                                'Failed to delete {0}/{1}: {2}'.format(
                                info['name'],
                                info['object_id'],
                                result['msg'],
                        ))

        # Perform the registration, if necessary
        if found_registration:
            return {'success': True, 'msg': 'Previously registered'}
        else:
            return self.parent.client.create_client(
                    name=registration_value,
                    proto='FC',
                    ip=self._REGISTRATION_IP,
                    client_os=self._REGISTRATION_OPERATING_SYSTEM,
                    clustered=False,
                    reserved=False,
            )

class UtilityManager02(UtilityManager01):
    _DEDUP_STATUS_PATH = '/monitor/status/dedup'

    @property
    def is_external_head(self):
        """Returns if this Concerto is an external head or not."""
        return self.parent.properties['hardware_model'] == 'R720'

    @property
    def is_mga(self):
        """Returns if this Concerto object is connected to MGA or not."""
        return self._get_mg_identity('mg-a')

    @property
    def is_mgb(self):
        """Returns if this Concerto object is connected to MGB or not."""
        return self._get_mg_identity('mg-b')

    def _get_mg_identity(self, value):
        """Internal worker function for:

            * is_mga
            * is_mgb

        """
        return self.parent.properties.get('slot_type', None) == value

    def get_dedup_status(self):
        """Gets the deduplication status.

        Returns:
            dict

        Raises:
            QueryError

        """
        ans = self.parent.basic.get(self._DEDUP_STATUS_PATH)
        if not ans['success']:
            raise QueryError(ans.get('msg', str(ans)))

        return ans['data']

    def is_dedup_enabled(self):
        """Returns if dedup is enabled or not."""
        try:
            ans = self.get_dedup_status()
        except QueryError:
            return False
        else:
            return True
