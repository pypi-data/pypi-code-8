import os
import time
import glob


class Temperature:
    temp_sensor_folder = ""

    def __init__(self):
        os.system('sudo modprobe w1-gpio')
        os.system('sudo modprobe w1-therm')
        base_dir = '/sys/bus/w1/devices/'
        self.tempSensorFolder = (glob.glob(base_dir + '28*')[0]) + '/w1_slave'

    def read_temp_raw(self):
        """Returns the raw temperature, not in human readable form"""

        f = open(self.temp_sensor_folder, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp_celsius(self):
        """Returns the temperature in celsius"""

        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            return float(temp_string) / 1000.0

    def read_temp_fahrenheit(self):
        """Returns the temperature in fahrenheit"""

        temp_f = self.read_temp_celsius() * 9.0 / 5.0 + 32.0
        return str(temp_f)
