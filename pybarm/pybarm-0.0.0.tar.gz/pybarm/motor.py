import RPi.GPIO as GPIO
from time import sleep
 
GPIO.setmode(GPIO.BCM)

class Motor:
    
    def __init__(self, a,b,e,rev_time=4.0):
        self.a = a
        self.b = b
        self.e = e
        self.revolution_time = rev_time
        self.seconds_per_degree = self.revolution_time / 360.0
        GPIO.setup(self.a, GPIO.OUT)
        GPIO.setup(self.b, GPIO.OUT)
        GPIO.setup(self.e, GPIO.OUT)
    
    def degrees_to_time(self,degrees):
        assert degrees, 'degrees value to convert to on time cannot be False'
        return self.seconds_per_degree * degrees
    
    def go_clockwise(self,degrees=False):
        GPIO.output(self.a,GPIO.HIGH)
        GPIO.output(self.b,GPIO.LOW)
        GPIO.output(self.e,GPIO.HIGH)
        if degrees:
            sleep(self.degrees_to_time(degrees))
            self.stop()
    
    def go_anticlockwise(self,degrees=False):
        GPIO.output(self.a,GPIO.LOW)
        GPIO.output(self.b,GPIO.HIGH)
        GPIO.output(self.e,GPIO.HIGH)
        if degrees:
            sleep(self.degrees_to_time(degrees))
            self.stop()
    
    def stop(self):
        GPIO.output(self.e,GPIO.LOW)
    
    def cleanup(self):
        GPIO.cleanup()

try:
    motor = Motor(4,17,18)
    motor.go_clockwise(360) 
    motor.go_anticlockwise(360)
    motor.stop()
    motor.cleanup()
except:
    GPIO.cleanup()