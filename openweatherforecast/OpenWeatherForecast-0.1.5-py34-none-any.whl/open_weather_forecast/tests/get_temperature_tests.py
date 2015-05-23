import unittest


class GetTemperatureTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://api.openweathermap.org/data/2.5/forecast/city?q={}'.format("London,uk")

    def tearDown(self):
        pass

    def basic_test(self):
        pass