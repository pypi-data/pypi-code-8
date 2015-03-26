# Copyright 2014 Isotoma Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from botocore import session


session = session.get_session({
    # Allow providing our own botocore json to override (and increase) various
    # timeouts
    "data_path": (
        'data_path',
        'BOTO_DATA_PATH',
        os.path.join(os.path.dirname(__file__), "data"),
    ),
})


# Force botocore to initialise - this avoids race conditions around
# get_component
session.create_client("ec2", "eu-west-1")


class Session(object):

    def __init__(self, access_key_id, secret_access_key, session_token, expiration, region):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.session_token = session_token
        self.expiration = expiration
        self.region = region

    def create_client(self, service):
        return session.create_client(
            service_name=service,
            region_name=self.region,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            aws_session_token=self.session_token,
        )
