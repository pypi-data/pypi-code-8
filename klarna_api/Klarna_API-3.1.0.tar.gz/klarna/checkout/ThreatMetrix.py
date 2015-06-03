''' Klarna API - checkout - ThreatMetrix

Threatmetrix integration
'''

# Copyright 2015 Klarna AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .checkouthtml import CheckoutHTML

template = '<p style="display: none; background:url(%(scheme)s://%(host)s/fp/'\
    'clear.png?org_id=%(orgid)s&amp;session_id=%(sid)s&amp;m=1);"></p>'\
    '<script src="%(scheme)s://%(host)s/fp/check.js?org_id=%(orgid)s&amp;'\
    'session_id=%(sid)s" type="text/javascript"></script>'\
    '<img src="%(scheme)s://%(host)s/fp/clear.png?org_id=%(orgid)s&amp;'\
    'session_id=%(sid)s&amp;m=2\" alt="" />'\
    '<object type="application/x-shockwave-flash" style="display: none" data='\
    '"%(scheme)s://%(host)s/fp/fp.swf?org_id=%(orgid)s&amp;session_id=%(sid)s" '\
    'width="1" height="1" id="obj_id">'\
    '<param name="movie" value="%(scheme)s://%(host)s/fp/fp.swf?org_id=%(orgid)s'\
    '&amp;session_id=%(sid)s" /><div></div></object>'


class ThreatMetrix(CheckoutHTML):
    # The ID used in conjunction with the Klarna API
    ID = 'dev_id_1'

    # ThreatMetrix organizational ID
    orgID = 'qicrzsu4'

    # Hostname used to access ThreatMetrix
    host = 'h.online-metrix.net'

    # Protocol used to access ThreatMetrix
    scheme = 'https'

    def __init__(self, klarna, eid, session=None):
        ''' Initialises ThreatMetrix integration
            session should be a dictionary-like object where session variables
            can be read and saved (e.g beaker session or pythonweb session)
        '''

        if session is None:
            self.session_id = self.get_session_id(eid)
        else:
            if self.ID not in session or len(session[self.ID]) < 40:
                session[self.ID] = self.session_id = self.get_session_id(eid)
            else:
                self.session_id = session[self.ID]

        klarna.set_session_id(self.ID, self.session_id)

    def clear(self, session):
        ''' Clears the ThreatMetrix session variable from the given
            dictionary-like session object
        '''

        session[self.ID] = None
        try:
            del session[self.ID]
        except:
            pass

    def to_html(self):
        info = {'scheme': self.scheme,
            'host': self.host,
            'orgid': self.orgID,
            'sid': self.session_id}

        return template % info
