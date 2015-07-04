# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import bluetooth
import logging


class Lazybone:
    port = 1
    sock = None
    bluetooth_bee = "BluetoothBee"
    addr = None

    def connect(self, addr):
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((addr, self.port))
        logging.info("%s Connected" % addr)
        self.addr = addr
        return True

    def find_name_addr(self, name):
        nearby_devices = bluetooth.discover_devices()
        for bdaddr in nearby_devices:
            dev_name = bluetooth.lookup_name(bdaddr)
            logging.debug(
                "Detected: %s while looking for %s" % (dev_name, name)
                )
            if name == dev_name:
                logging.info("Found: %s at %s" % (name, bdaddr))
                return bdaddr
        logging.info("Not Found: %s" % name)
        return None

    def connect_name(self, name):
        addr = self.find_name_addr(name)
        if addr is not None:
            return self.connect(addr)
        return False

    def connect_bluetooth_bee(self):
        return self.connect_name(self.bluetooth_bee)

    def check_connected(self):
        if self.addr is None:
            raise LazyboneError("Lazybone must first be connected")

    def on(self):
        self.check_connected()
        logging.info("%s Switching to ON", self.addr)
        try:
            self._on()
        except bluetooth.btcommon.BluetoothError:
            if self.reconnect():
                return self._on()
            raise LazyboneError("Lazybone connection lost. Couldn't reconnect.")

    def _on(self):
        return self.sock.send("e")

    def off(self):
        self.check_connected()
        logging.info("%s Switching to OFF", self.addr)
        try:
            self._off()
        except bluetooth.btcommon.BluetoothError:
            if self.reconnect():
                return self._off()
            raise LazyboneError("Lazybone connection lost. Couldn't reconnect.")

    def _off(self):
        return self.sock.send("o")

    def reconnect(self):
        logging.info("Connect lost to Lazybone. Attempting reconnect...")
        addr = self.addr
        self.close()
        return self.connect(addr)

    def close(self):
        if self.addr is not None:
            self.sock.close()
            logging.info("%s Disconnected" % self.addr)
            return True
        logging.debug("Nothing to close")
        return False


class LazyboneError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
        self.message = message
