# Copyright:: Copyright (c) 2015 PagerDuty, Inc.
# License:: Apache License, Version 2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and

import sys
import xmlrpclib


class Confluence(object):

    def __init__(self, url, user, password):
        self.server = xmlrpclib.ServerProxy(url)
        self.token = self.server.confluence2.login(user, password)

    def get_page(self, space, pageName):
        try:
            page = self.server.confluence2.getPage(self.token, space, pageName)
            return page
        except Exception as e:
            return None

    def update_page(self, page):
        try:
            page = self.server.confluence2.storePage(self.token, page)
            return page
        except Exception as e:
            sys.stderr.write("Page update failed. " + e.message)
