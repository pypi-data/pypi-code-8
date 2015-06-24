__author__ = 'Stephan Conrad <stephan@conrad.pics>'

from dbus import SystemBus, SessionBus, Interface
from time import sleep

class Service(object):

    def __init__(self, name, description=None,
                 load=None, active=None, subState=None, path=None, interface = None, proxy = None, enabled = False):
        self.name = name
        self.description = description
        self.loadState = load
        self.activeState = active
        self.subState = subState
        self.objectPath = path
        self.interface = interface
        self.proxy = proxy
        self.enabled = enabled
        self.running = self.activeState == 'active'
        self._manager = None

    def __repr__(self):
        return '{name = %s, description = %s, load state = %s, active state = %s, sub state = %s, object path = %s}' %(
            self.name, self.description, self.loadState, self.activeState, self.subState, self.objectPath
        )

    def _realoadProperties(self):
        if self.proxy != None:
            self.loadState = self.proxy.Get('org.freedesktop.systemd1.Unit', 'LoadState', dbus_interface='org.freedesktop.DBus.Properties')
            self.activeState = self.proxy.Get('org.freedesktop.systemd1.Unit', 'ActiveState', dbus_interface='org.freedesktop.DBus.Properties')
            self.subState = self.proxy.Get('org.freedesktop.systemd1.Unit', 'SubState', dbus_interface='org.freedesktop.DBus.Properties')
            self.enabled = self._getManager().GetUnitFileState(self.name).lower() == 'enabled'
            self.running = self.activeState == 'active'

    def _getManager(self):
        if self._manager == None:
            bus = SystemBus()
            self._manager = Interface(
                bus.get_object(
                    'org.freedesktop.systemd1',
                    '/org/freedesktop/systemd1'
                ),
                dbus_interface='org.freedesktop.systemd1.Manager'
            )
        return self._manager

    def enable(self):
        manager = self._getManager()
        manager.EnableUnitFiles([self.name], False, False)
        self._realoadProperties()
        return self.enabled


    def disable(self):
        manager = self._getManager()
        manager.DisableUnitFiles([self.name], False)
        self._realoadProperties()
        if self.enabled == False:
            return True
        return False

    def start(self):
        self.interface.Start('fail')
        while not self.running:
            sleep(1)
            self._realoadProperties()
            if self.activeState == 'failed':
                return False
        return self.running


    def stop(self):
        if self.running:
            self.interface.Stop('fail')
            while self.activeState != 'inactive':
                sleep(1)
                self._realoadProperties()
            return self.activeState == 'inactive'
        return False

    def restart(self):
        self.stop()
        return self.start()

class Services(object):

    def __init__(self):
        self.bus = SystemBus()
        self.manager = Interface(
            self.bus.get_object('org.freedesktop.systemd1',
                         '/org/freedesktop/systemd1'),
            dbus_interface='org.freedesktop.systemd1.Manager'
        )
        self._serviceList = {}
        self.subStates = set()

    def listUnits(self):
        self._serviceList.clear()
        for unit in self.manager.ListUnits():
            name = str(unit[0])
            if name.endswith('.service'):
                s = Service(
                    name=name,
                    description=unit[1],
                    load=unit[2],
                    active=unit[3],
                    subState=unit[4],
                    path=unit[6]
                )
                if s.subState == 'running':
                    self.subStates.add(s.name)
                self._serviceList[name] = s
        return self._serviceList

    def getServiceByName(self, serviceName):
        if len(self._serviceList) == 0:
            self.listUnits()
        if serviceName in self._serviceList:
            o = self._serviceList[serviceName]
            proxy = self.bus.get_object(
                    'org.freedesktop.systemd1',
                    o.objectPath
                )
            service = Interface(
                proxy,
                dbus_interface='org.freedesktop.systemd1.Unit'
            )
            o.interface = service
            o.proxy = proxy
            o._realoadProperties()
            self._serviceList[serviceName] = o
            return o
        return None


if __name__ == "__main__":
    s = Services()
    s.listUnits()
    o = s.getServiceByName('httpd.service')
    print(o.enable())
    sleep(10)
    print(o.disable())