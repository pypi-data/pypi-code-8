import unittest
import random

import numpy as np

import client


class TestClient(unittest.TestCase):

    def test_echo(self):
        array_size = 60 * 24 * 14
        x = np.array(
            [random.random() for _ in range(array_size)],
            dtype='f'
        )

        ret = client.call_model('http://127.0.0.1:8889/echo', x)

        # they should be very close to the same
        self.assertTrue(np.all((x - ret) < 1e-7))

        # they should be exactly the same
        self.assertTrue(np.all(x == ret))

    def test_ev(self):
        array_size = 60 * 24 * 14 * 1
        x = np.array(
            [random.random() for _ in range(array_size)],
            dtype='f'
        )

        # host = '10.51.131.7'
        host = 'ec2-54-82-32-235.compute-1.amazonaws.com'
        url = 'http://{host}:8889/ev'.format(host=host)
        ret = client.call_model(url, x)

        self.assertTrue(ret is not None)


if __name__ == '__main__':
    unittest.main()
