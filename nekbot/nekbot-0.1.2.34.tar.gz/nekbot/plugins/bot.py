# coding=utf-8
import platform
from nekbot.core.commands import command
from nekbot.core.commands.control import control
from nekbot.utils.human import strdelta
from nekbot.utils.timeutils import since
from nekbot.utils import system

__author__ = 'nekmo'


@command
def about(msg):
    """Información sobre este bot.
    """
    body = u'⚛ Este bot funciona gracias a NekBot %s bajo Python %s. Protocolos en uso: %s' % (
        msg.protocol.nekbot.version, platform.python_version(),
        ', '.join([protocol for protocol in msg.protocol.nekbot.protocols.modules_names])
    )
    msg.reply(body)


@command
def uptime(msg):
    """Tiempo que llevo conectado. {usage}
    """
    return strdelta(since(msg.protocol.nekbot.start_datetime))


@command
@control('root')
def reboot(msg):
    """Reboot bot. {usage}
    """
    msg.reply('Rebooting!')
    msg.protocol.nekbot.close()
    system.reboot()

@command
@control('root')
def shutdown(msg):
    """Shutdown bot. {usage}
    """
    msg.reply('Shutdown!')
    msg.protocol.nekbot.close()