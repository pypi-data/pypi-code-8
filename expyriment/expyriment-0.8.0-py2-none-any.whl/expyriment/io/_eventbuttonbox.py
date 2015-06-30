"""
An event button box.

This module contains a class implementing an event button box.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = '0.8.0'
__revision__ = '19b141b'
__date__ = 'Tue Jun 30 17:14:58 2015 +0200'


from _streamingbuttonbox import StreamingButtonBox


class EventButtonBox(StreamingButtonBox):
    """A class implementing an event button box input."""

    def __init__(self, interface):
        """Create an event button box input.

        Compared to a StreamingButtonBox, an EventButtonBox has no baseline
        (baseline=None). The methods wait() and check() are therefore
        responsive to every incomming interface event.

        Parameters
        ----------
        interface : io.SerialPort or io.ParallelPort
            an interface object

        """

        StreamingButtonBox.__init__(self, interface, None)

    @property
    def baseline(self):
        """Getter for baseline"""
        return self._baseline

    @baseline.setter
    def baseline(self, value):
        """Setter for baseline."""
        print("Warning: A baseline cannot be defined for an EventButtonBox!")
        self._baseline = None
