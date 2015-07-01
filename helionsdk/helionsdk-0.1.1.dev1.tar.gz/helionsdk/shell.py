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

"""
Run Helion SDK Plugin

Run this script and it creates an OpenStack SDK Connection object and loads
the helionsdk plugin.
"""

import os
import sys

import os_client_config

from openstack import connection
from openstack import profile


def main(argv=sys.argv[1:]):
    os_cloud = os.environ.get('OS_CLOUD')
    cloud = os_client_config.OpenStackConfig().get_one_cloud(os_cloud)
    auth = cloud.config['auth']
    prof = profile.Profile(extensions=['helionsdk.dns'])
    conn = connection.Connection(profile=prof, **auth)
    for domain in conn.dns.list_domains():
        print(str(domain))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
