__author__ = 'victor'
import json
from pprint import pprint
from matplotlib import pylab as P

class Monitor(object):
    """ Abstraction to monitor a stream of data
    On creation, the file log is rewritten if it exists

    :ivar name: name of the monitor
    :ivar log_file: string path to the log file
    :ivar log_file_handle: file handle to the log file
    """

    def __init__(self, name, log_file):
        self.name = name
        self.log_file = log_file
        self.log_file_handle = open(log_file, 'wb')

    def write(self, values):
        """ writes values to the log file in json form

        :param values: dictionary of values to write to disk
        """
        self.log_file_handle.write(json.dumps(values) + "\n")
        self.log_file_handle.flush()

    @classmethod
    def read_log_file(cls, log_file):
        """ reconstructs the data sequence from a log file

        :param log_file: string path to the log file
        """
        with open(log_file, 'rb') as f:
            lines = f.readlines()
        data = {}
        for l in lines:
            d = json.loads(l.strip("\n"))
            for k, v in d.items():
                if k not in data: data[k] = [v]
                else: data[k] += [v]
        return data

    def read(self):
        """ reconstructs the data sequence from the internal log file
        """
        return self.__class__.read_log_file(self.log_file)

    def close(self):
        """ close log file handle
        """
        self.log_file_handle.close()


class Logger(object):
    """ Utility for monitoring, logging and plotting data streams

    :ivar watched: a dictionary of ``Monitors`` monitored
    :ivar stdout: if ``True``, will print to stdout in addition to log files
    """

    def __init__(self, stdout=True):
        self.watched = {}
        self.stdout = stdout

    def watch(self, monitor):
        """ adds a ``Monitor`` to watch
        """
        self.watched[monitor.name] = monitor

    def push(self, name, **values):
        """ pushes a unpacked stream of key-value pairs to the specified ``Monitor``

        :param name: name of the ``Monitor`` to stream to
        :param values: unpacked stream of key-value pairs
        """
        if self.stdout:
            pprint(values)
        self.watched[name].write(values)

    def plot(self, name, x_var, y_var, plot_func=P.plot, pre_plot=None, post_plot=None, to_file=None):
        """ generates a plot for the specified monitor

        :param name: name of the ``Monitor`` to plot
        :param x_var: key of the streamed variable to plot on the x axis
        :param y_var: key of the streamed variable to plot on the y axis
        :param plot_func: function to use for plotting, default is ``pylab.plot``
        :param pre_plot: function to run before plotting
        :param post_plot: function to run after plotting
        :param to_file: file to save the plot in
        """
        watched = self.watched[name]
        fig = P.figure()
        if pre_plot is None:
            P.title("%s vs %s" % (x_var, y_var))
            P.xlabel(x_var)
            P.ylabel(y_var)
        else:
            pre_plot()
        data = watched.read()
        plot_func(data[x_var], data[y_var])
        if post_plot is not None:
            post_plot()
        if to_file is None:
            to_file = watched.log_file + 'png'
        P.savefig(to_file)
        P.close(fig)

    def close(self, name):
        """ close specified ``Monitor``

        :param name: if ``all``, all ``Monitor`` s are closed
        """
        if name == 'all':
            for name, w in self.watched.items():
                w.close()
        else:
            self.watched[name].close()
