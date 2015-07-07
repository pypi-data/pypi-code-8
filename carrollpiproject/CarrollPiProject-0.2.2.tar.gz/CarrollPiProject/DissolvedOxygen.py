import serial


class dissolved_oxygen:
    ser = ""

    def __init__(self):
        ser = serial.Serial('/dev/ttyAMA0', 38400)

    def turn_on_lights(self):
        """Turns on the LED for debugging"""
        self.ser.write("L,1<CR>")

    def pass_temperature(self, temp):
        """Passes the temperature to the DO sensor for a more accurate reading

        Args: \n
        :param temp: the temperature in Celsius \n
        :type temp: str \n
        """
        self.ser.write("T," + str(temp) + "<CR>")

    def get_data(self):
        """Sends a request for Dissolved Oxygen data then interprets and returns the response"""

        self.ser.write("C")

        line = ""

        data = self.ser.read()
        while (data != '\r'):
            line = line + data
            data = self.ser.read()

        return line
