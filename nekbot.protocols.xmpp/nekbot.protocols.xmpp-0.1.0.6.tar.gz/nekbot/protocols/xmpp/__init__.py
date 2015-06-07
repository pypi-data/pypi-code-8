from collections import defaultdict
from logging import getLogger
import sleekxmpp
import sys
import time
from nekbot import settings
from nekbot.protocols.base import ProtocolBase
from nekbot.protocols.xmpp.message import XMPPMessage
from nekbot.protocols.xmpp.user import UserXMPP
from sleekxmpp import plugins
from xml.etree import cElementTree as ET


__author__ = 'nekmo'

logger = getLogger('nekbot.protocols.xmpp')

if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding

    setdefaultencoding('utf8')


class XMPP(sleekxmpp.ClientXMPP, ProtocolBase):
    features = ['newline', 'groupchats', 'history']
    user_class = UserXMPP
    name = 'XMPP'

    def __init__(self, nekbot):
        plugin_whitelist = plugins.__all__
        plugin_blacklist = settings.XMPP_PLUGIN_BLACKLIST
        for plugin in plugin_blacklist:
            plugin_whitelist.remove(plugin)
        sleekxmpp.ClientXMPP.__init__(self, settings.XMPP_JID, settings.XMPP_PASSWORD,
                                      plugin_config=self.get_plugin_config(),
                                      plugin_whitelist=plugin_whitelist, escape_quotes=True, sasl_mech=None, lang='en')
        ProtocolBase.__init__(self, nekbot)

    def get_plugin_config(self):
        # config = defaultdict(defaultdict)
        config = {}
        if True:
            config['xep_0048'] = {}
            config['xep_0048']['auto_join'] = True
        return config

    def prepare_message(self, body):
        if not isinstance(body, (str, unicode)):
            body = unicode(body)
        try:
            body = body.decode('utf-8')
        except:
            pass
        return body

    def sleek_send_message(self, mto, mbody, msubject=None, mtype=None,
                           mhtml=None, mfrom=None, mnick=None):
        return sleekxmpp.ClientXMPP.send_message(self, mto, mbody, msubject, mtype, mhtml, mfrom, mnick)

    def join_room(self, jid, nick=None, password=None):
        self.plugin['xep_0045'].joinMUC(jid, nick, password, wait=True)

    def join_rooms(self):
        for room in settings.XMPP_GROUPCHATS:
            self.join_room(**room)

    def start(self):
        self.register_plugins()
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.connect()
        self.process()
        self.join_rooms()
        # time.sleep(40)

    def message(self, msg):
        self.propagate('message', XMPPMessage(self, msg))

    def session_start(self, session):
        self.send_presence()
        self.get_roster()

    def close(self):
        logger.debug('Closing SleekXMPP...')
        self.disconnect()


Xmpp = XMPP