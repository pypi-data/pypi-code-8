# Copyright © 2013-2015 Andrew Wilcox and Elizabeth Myers.
# All rights reserved.
# This file is part of the PyIRC 3 project. See LICENSE in the root directory
# for licensing information.


"""DCC base classes"""


from logging import getLogger

from PyIRC.extension import BaseExtension
from PyIRC.hook import hook
from PyIRC.event import EventState, Event, LineEvent
from PyIRC.numerics import Numerics
from PyIRC.auxparse import CTCPMessage
from PyIRC.util.version import versionstr


logger = getLogger(__name__)


class DCCEvent(Event):

    """A DCC event"""


class DCCChatEvent(LineEvent, Event):

    """A DCC chat event"""


class DCCHandler(BaseExtension):

    """Handler for basic DCC functions."""

    hook_classes = {
        "dcc_chat", DCCChatEvent,
    }

    requires = ["CTCP"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @hook("commands_ctcp", "DCC")
    def dcc_handler(self, event):
        pass

