#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbus

"""
http://www.documentroot.net/en/linux/python-dbus-tutorial
https://developer.pidgin.im/wiki/DbusHowto
"""

class DbusClient(dbus.service.Object):
    def __init__(self, object_path):
        dbus.service.Object.__init__(self, dbus.SessionBus(), path)
