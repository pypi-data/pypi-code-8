__author__ = 'Kyle'

import RPi.GPIO as GPIO
import math
import time

class Sensor:

    def __init__(self, port):
        self.port = port

    def resistance(self):
        GPIO.setmode(GPIO.BOARD)
        measurement = 0
        GPIO.setup(self.port, GPIO.OUT)
        GPIO.output(self.port, GPIO.LOW)
        time.sleep(0.1)
        GPIO.setup(self.port, GPIO.IN)
        while GPIO.input(self.port) == GPIO.LOW:
            measurement += 1
        return measurement


class Temperature(Sensor):
    """Represent a temperature sensor."""

    def getTempF(self):
        total = 0
        for _ in range(30):
            total += self.resistance()
        y = total/30.0
        a = 0.17
        b = -40
        c = 2615 - y
        return (-b - math.sqrt(b**2 - 4 * a * c))/(2 * a)
    
    def getTempC(self):
        return (getTempF(self.port) - 32) * (5/9.0)


class Light(Sensor):
    """Represent a light sensor."""

    def isDark(self):
        if self.resistance() > 20000:
            return True
        return False

    def isLight(self)
        return not self.isDark()
