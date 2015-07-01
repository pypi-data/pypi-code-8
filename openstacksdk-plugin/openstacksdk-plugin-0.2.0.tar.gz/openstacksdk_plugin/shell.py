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
Run Example Plugin

Run this script and it creates an OpenStack SDK Connection object and loads
the openstacksdk_plugin example.  It prints 'hello' and 'goodbye' using the
the example plugin proxy.  To keep things simple, this example only works
with os-client-configuration  It doesn't need to authenticate at all, but
it needs to build a proper connection.
"""

import os
import sys

from openstack import connection
from openstack import profile
import os_client_config


def main(argv=sys.argv[1:]):
    os_cloud = os.environ.get('OS_CLOUD')
    cloud = os_client_config.OpenStackConfig().get_one_cloud(os_cloud)
    auth = cloud.config['auth']
    if not auth:
        print("ERROR: No valid authentication information was found.")
        print("       The cloud name you want to use should be set")
        print("       and exported with the OS_CLOUD environment variable.")
        print("       Authentication is not required to run this script")
        print("       but all the information to authenticate is needed")
        print("       to create an OpenStack SDK Connection")
        print("")
        print("For more on OpenStack Cloud Configuration:")
        print("http://docs.openstack.org/developer/os-cloud-config/")
        print("")
        print("Feel free to copy this script and modify it to your tastes.")
        sys.exit(1)
    prof = profile.Profile(extensions=['openstacksdk_plugin.example'])
    conn = connection.Connection(profile=prof, **auth)
    print(conn.example.return_hello())
    print(conn.example.return_goodbye())


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
