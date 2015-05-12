import lightblue
from nxt import Motor, find_one_brick, PORT_A, PORT_B, PORT_C, PORT_1, PORT_2, PORT_3, PORT_4
from nxt.sensor import Touch, Sound, Ultrasonic, Light
from time import sleep

class PortMap(dict):
    def __init__(self, ports, factory):
        self.factory = factory
        self.ports = ports
    def __missing__(self, port):
        if port in self.ports:
            self[port] = self.factory(port)
            return self[port]
        else:
            raise ValueError("{} is an invalid port; must be one of {}".format(
                    port, ", ".join(self.ports)))

class NXTBrick():
    motorPorts = {
        "a": PORT_A,
        "b": PORT_B,
        "c": PORT_C
    }

    sensorPorts = {
        1: PORT_1,
        2: PORT_2,
        3: PORT_3,
        4: PORT_4
    }

    sensorTypes = {
        "none" : None,
        "touch" : Touch,
        "sound" : Sound,
        "ultrasonic" : Ultrasonic,
        "light" : Light
    }

    def __init__(self):
        self.brick = find_one_brick()
        self.motors = PortMap(self.motorPorts.keys(), self._motor_factory())
        self.sensors = {}

    def roll(self, port, power):
        self.motors[port].run(max(-100, min(100, power)))

    def halt(self, port):
        self.motors[port].brake()
        sleep(0.2)
        self.motors[port].idle()

    def read_sensor(self, port):
        if port in self.sensors.keys():
            return int(self.sensors[port].get_sample())
        else:
            return "None"

    def read_sensors(self):
        return {i: self.read_sensor(i) for i in self.sensorPorts.keys()}

    def _motor_factory(self):
        def create_motor(port):
            return Motor(self.brick, self.motorPorts[port])
        return create_motor

    def add_sensor(self, port, sensorType):
        if port in self.sensorPorts.keys() and sensorType in self.sensorTypes:
            if sensorType == 'none': 
                del self.sensors[port]
            else:
                self.sensors[port] = self.sensorTypes[sensorType](
                        self.brick, self.sensorPorts[port])
                if sensorType == 'light':
                    self.sensors[port].set_illuminated(True)
        else:
            if port not in self.sensorPorts.keys():
                raise ValueError("{} is an invalid sensor port; must be in {}".format(
                        port, ", ".join(map(str, self.sensorPorts.keys()))))
            else:
                raise ValueError("{} is an invalid sensor type; must be in {}".format(
                        sensorType, ", ".join(self.sensorTypes)))

    def remove_sensor(self, port):
        self.add_sensor(port, 'none')






