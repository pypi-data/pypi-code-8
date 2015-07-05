# -*- coding: utf-8 -*-
# (c) 2015 Tuomas Airaksinen
#
# This file is part of automate-arduino.
#
# automate-arduino is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# automate-arduino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with automate-arduino.  If not, see <http://www.gnu.org/licenses/>.

import os
import threading

from automate import Lock
from traits.api import HasTraits, Any, Dict, CList, Str, Int, List
from automate.service import AbstractSystemService


class ArduinoService(AbstractSystemService):

    """
        Service that provides interface to Arduino devices via
        `pyFirmata library <https://github.com/tino/pyFirmata>`_.
    """

    #: Arduino devices to use, as a list
    arduino_devs = CList(Str, ["/dev/ttyUSB0"])

    #: Arduino device board types, as a list of strings. Choices are defined by pyFirmata board
    #: class names, i.e. allowed values are "Arduino", "ArduinoMega", "ArduinoDue".
    arduino_dev_types = CList(Str, ["Arduino"])

    #: Arduino device sampling rates, as a list (in milliseconds).
    arduino_dev_sampling = CList(Int, [500])

    _sens_analog = Dict
    _sens_digital = Dict
    _act_analog = Dict
    _act_digital = Dict
    _boards = List
    _locks = List
    _iterator = Any

    def setup(self):
        self.logger.debug("Initializing Arduino subsystem")
        try:
            import pyfirmata
        except ImportError:
            self.logger.error("Please install pyfirmata if you want to use Arduino interface")
            return

        # Patch Pin class in pyfirmata to have Traits. Particularly, we need notification for value changes in Pins.

        PinOld = pyfirmata.Pin

        class Pin(PinOld, HasTraits):
            mode = property(PinOld._get_mode, PinOld._set_mode)

            def __init__(self, *args, **kwargs):
                HasTraits.__init__(self)
                self.add_trait("value", Any)
                PinOld.__init__(self, *args, **kwargs)

        import pyfirmata.pyfirmata

        pyfirmata.Pin = Pin
        pyfirmata.pyfirmata.Pin = Pin

        import pyfirmata.util

        # Patching also Iterator as it does not quit cleanly when exiting.

        class FixedPyFirmataIterator(pyfirmata.util.Iterator):

            def run(iter_self):
                try:
                    super(FixedPyFirmataIterator, iter_self).run()
                except Exception as e:
                    self.logger.error('Exception %s occurred in Pyfirmata iterator, quitting now', e)
                    self.logger.error('threads: %s', threading.enumerate())

        # Initialize configured self.boards
        ard_devs = self.arduino_devs
        ard_types = self.arduino_dev_types
        samplerates = self.arduino_dev_sampling
        assert len(ard_devs) == len(ard_types) == len(samplerates), 'Arduino configuration invalid!'

        class FileNotReadableError(Exception):
            pass

        for i in xrange(len(ard_devs)):
            try:
                if not os.access(ard_devs[i], os.R_OK):
                    raise FileNotReadableError
                cls = getattr(pyfirmata, ard_types[i])
                board = cls(ard_devs[i])
                board.send_sysex(pyfirmata.SAMPLING_INTERVAL, pyfirmata.util.to_two_bytes(samplerates[i]))
                self._iterator = it = FixedPyFirmataIterator(board)
                it.name = "PyFirmata thread for {dev}".format(dev=ard_devs[i])
                it.start()
                board._iter = it
                self._boards.append(board)
            except (FileNotReadableError, OSError) as e:
                if isinstance(e, FileNotReadableError) or e.errno == os.errno.ENOENT:
                    self.logger.warning('Your arduino device %s is not available. Arduino will be mocked.', ard_devs[i])
                    self._boards.append(None)
                else:
                    raise e
            self._locks.append(Lock())

    def cleanup(self):
        self.logger.debug("Cleaning up Arduino subsystem. ")
        for board in self._boards:
            if board:
                board.exit()
        if self._iterator:
            self._iterator.board = None

    def setup_digital(self, dev, pin_nr):
        if not self._boards[dev]:
            return
        with self._locks[dev]:
            pin = self._boards[dev].get_pin("d:{pin}:o".format(pin=pin_nr))
            self._act_digital[(dev, pin_nr)] = pin

    def setup_pwm(self, dev, pin_nr):
        if not self._boards[dev]:
            return
        with self._locks[dev]:
            pin = self._boards[dev].get_pin("d:{pin}:p".format(pin=pin_nr))
            self._act_digital[(dev, pin_nr)] = pin

    def setup_servo(self, dev, pin_nr, min_pulse, max_pulse, angle):
        if not self._boards[dev]:
            return
        with self._locks[dev]:
            pin = self._boards[dev].get_pin("d:{pin}:s".format(pin=pin_nr))
            self._act_digital[(dev, pin_nr)] = pin
            self._boards[dev].servo_config(pin_nr, min_pulse, max_pulse, angle)

    def change_digital(self, dev, pin_nr, value):
        """ Change digital Pin value (boolean). Also PWM supported(float)"""
        if not self._boards[dev]:
            return
        with self._locks[dev]:
            self._act_digital[(dev, pin_nr)].write(value)

    # Functions for input signals
    def handle_analog(self, obj, name, old, new):
        dev = obj.__dev_id
        pin = obj.pin_number
        if not self._boards[dev]:
            return
        self._sens_analog[(dev, pin)][0].set_status(new)

    def handle_digital(self, obj, name, old, new):
        dev = obj.__dev_id
        pin = obj.pin_number
        if not self._boards[dev]:
            return
        self._sens_digital[(dev, pin)][0].set_status(new)

    def subscribe_analog(self, dev, pin_nr, sens):
        if not self._boards[dev]:
            return
        with self._locks[dev]:
            pin = self._boards[dev].get_pin("a:{pin}:i".format(pin=pin_nr))
            pin.__dev_id = dev
            self._sens_analog[(dev, pin_nr)] = (sens, pin)
            s = pin.read()
        if s is not None:
            sens.set_status(s)
        pin.on_trait_change(self.handle_analog, "value")

    def cleanup_digital_actuator(self, dev, pin_nr):
        pin = self._act_digital.pop((dev, pin_nr), None)

    def unsubscribe_digital(self, dev, pin_nr):
        pin = self._sens_digital.pop((dev, pin_nr), None)
        if pin:
            pin[1].remove_trait('value')

    def unsubscribe_analog(self, dev, pin_nr):
        pin = self._sens_analog.pop((dev, pin_nr), None)
        if pin:
            pin[1].remove_trait('value')

    def subscribe_digital(self, dev, pin_nr, sens):
        if not self._boards[dev]:
            return
        with self._locks[dev]:
            pin = self._boards[dev].get_pin("d:{pin}:i".format(pin=pin_nr))
            pin.__dev_id = dev
            self._sens_digital[(dev, pin_nr)] = (sens, pin)
            s = pin.read()
        if s is not None:
            sens.set_status(s)
        pin.on_trait_change(self.handle_digital, "value")
