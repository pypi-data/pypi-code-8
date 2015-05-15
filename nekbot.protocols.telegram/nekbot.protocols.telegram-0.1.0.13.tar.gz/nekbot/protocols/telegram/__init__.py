from logging import getLogger
import os
import pytg2
from pytg2.utils import coroutine
from nekbot.core import event
from nekbot.protocols.base.event import Event
from nekbot.protocols import Protocol
from nekbot.protocols.telegram.group_chat import GroupChatsTelegram
from nekbot.protocols.telegram.message import MessageTelegram
from nekbot.protocols.telegram.user import UserTelegram
import telejson

__author__ = 'nekmo'

telejson_dir = os.path.dirname(os.path.abspath(telejson.__file__))

TELEGRAM_BIN = '/home/nekmo/Src/tg-for-pytg2/bin/telegram-cli'
TELEGRAM_PUB = os.path.abspath(os.path.join(telejson_dir, 'tg-server.pub'))


logger = getLogger('nekbot.protocols.telegram')

EVENTS_TYPES = {
    'message': ['message', MessageTelegram],
    'chat_info': ['telegram.chat_info', Event],
}


@event('telegram.chat_info')
def chat_info(protocol, ev):
    groupchat = protocol.groupchats.get_or_create(ev.data.id, ev.data)
    groupchat.users.clear()
    groupchat.users.update({user.id: UserTelegram(protocol, user) for user in ev.data.members})
    print(groupchat.users)

class Telegram(Protocol):
    features = ['newline', 'groupchats', 'historical']
    tg = None
    receiver = None
    sender = None

    def init(self):
        self.tg = pytg2.Telegram(
            telegram=TELEGRAM_BIN,
            pubkey_file=TELEGRAM_PUB)
        self.receiver = self.tg.receiver
        self.sender = self.tg.sender

    def prepare_message(self, body):
        if not isinstance(body, (str, unicode)):
            body = str(body)
        try:
            body = body.decode('utf-8')
        except:
            pass
        return body

    def run(self):
        @coroutine  # from pytg2.utils import coroutine
        def handler():
            while not self.nekbot.is_quit:
                stanza = (yield)
                event_name, stanza_class = EVENTS_TYPES.get(stanza.event)
                if event_name is None:
                    logger.warning('unsupported type: %s' % stanza.event)
                    continue
                self.propagate(event_name, stanza_class(self, stanza))
        self.receiver.start()
        self.receiver.message(handler())

    def close(self):
        logger.debug('Closing Telegram-cli...')
        # l = threading.Thread(target=self.sender.safe_quit)
        # l.daemon = True
        # l.start()
        # l.join(5)
        # logger.debug('Send terminate signal to sender...')
        # self.sender.terminate()
        # logger.debug('Send stop signal to receiver...')
        # self.receiver.stop()
        # self.sender.s.close()
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.connect(('127.0.0.1', 4458))
        # s.close()