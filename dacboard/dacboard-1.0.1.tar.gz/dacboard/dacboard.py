#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (c) 2015 Michael Andersen

import serial

class DACException(Exception):
    """
    Thrown by DACBoard if something goes wrong
    """
    pass

class DACBoard(object):
    def __init__(self, device="/dev/ttyUSB0"):
        """
        Open the DAC board via the given serial device
        """
        self._handle = serial.Serial(device, 115200, timeout=1)
        self.reset()
        self.self_test()
        self.reset()

    def reset(self):
        """
        Reset the device to 0V output and reenable the overvoltage
        lockout
        """
        self._handle.write("R\n")
        line = self._handle.readline()
        if not line.startswith("SOK"):
            raise DACException("Inconsistent reset: " + line)
        line = self._handle.readline()
        if not line.startswith("RVR"):
            raise DACException("Inconsistent reset: " + line)
        self._version = line[4:]
        line = self._handle.readline()
        if not line.startswith("RME"):
            raise DACException("Inconsistent reset: " + line)
        line = self._handle.readline()
        if not line.startswith("ROK"):
            raise DACException("Inconsistent reset: " + line)

    def self_test(self):
        """
        This tests the DAC by writing a value to temp register and
        reading it back. Every set_voltage command does this as well
        so it doesn't add that much
        """
        self._handle.write("T\n")
        line = self._handle.readline()
        if not line.startswith("TOK"):
            raise DACException("Failed self test: " + line)

    def set_voltage(self, uV):
        """
        Sets the voltage of the DAC board in microvolts. Note that
        the resolution of the board is about 15.625 uV so the board will
        round to the nearest value that it can handle.
        """
        self._handle.write("S %d\n" % int(uV))
        line = self._handle.readline()
        if not line.startswith("SOK"):
            raise DACException("Failed set: " + line)

    def disable_overvoltage_lockout(self):
        """
        By default, after reset, the board will not allow outputting more
        than 500mV as this is the stated maximum of the Physitemp device.
        If you disable the overvoltage protection, you can output up to
        1.024 V
        """
        self._handle.write("U allow overvoltage\n")
        line = self._handle.readline()
        if not line.startswith("UOK"):
            raise DACException("Failed unlock: " + line)
