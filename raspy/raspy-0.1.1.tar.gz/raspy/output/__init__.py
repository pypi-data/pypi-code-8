__author__ = "Kyle"

import RPi.GPIO as GPIO
import time

class Output:

    def __init__(self, port):
        self.port = port

class LED(Output):

    TIME_UNIT = 0.2

    morse = {
        'a':'01',
        'b':'1000',
        'c':'1010',
        'd':'100',
        'e':'0',
        'f':'0010',
        'g':'110',
        'h':'0000',
        'i':'00',
        'j':'0111',
        'k':'101',
        'l':'0100',
        'm':'11',
        'n':'10',
        'o':'111',
        'p':'0110',
        'q':'1101',
        'r':'010',
        's':'000',
        't':'1',
        'u':'001',
        'v':'0001',
        'w':'011',
        'x':'1001',
        'y':'1011',
        'z':'1100'
        }

    def on(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.port, GPIO.OUT)
        GPIO.output(self.port, GPIO.HIGH)

    def off(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.port, GPIO.OUT)
        GPIO.setup(self.port, GPIO.LOW)

    def set(self, value):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.port, GPIO.OUT)
        p = GPIO.PWM(self.port, 60)
        p.start(value)

    def transToMorse(self, sentence):
        for word in sentence.lower().split():
            for letter in word:
                for signal in self.morse[letter]:
                    if signal == '0':
                        self.on()
                        time.sleep(self.TIME_UNIT)
                    else:
                        self.on()
                        time.sleep(self.TIME_UNIT * 3)
                    self.off()
                    time.sleep(self.TIME_UNIT)
                time.sleep(3 * self.TIME_UNIT)
            time.sleep(7 * self.TIME_UNIT)
            

class Motor(Output):

    def on(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.port, GPIO.OUT)
        GPIO.output(self.port, GPIO.HIGH)

    def off(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.port, GPIO.OUT)
        GPIO.setup(self.port, GPIO.LOW)
        
    def set(self, value):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.port, GPIO.OUT)
        p = GPIO.PWM(self.port, 60)
        p.start(value)
