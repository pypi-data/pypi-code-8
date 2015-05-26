# Python 2/3 support for loading ConfigParser
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import socket

class DaemonConfig(object):
    """ The configuration container for the daemon """

    def __init__(self, path):
        """ Create a new daemon configuration context """

        parser = configparser.RawConfigParser()
        parser.read(path)

        # Configuration options specific to interacting with InfluxDB
        self.influxdb = {
            'version': parser.get('InfluxDB', 'ServerVersion') or '0.8',

            # Get server connection info
            'host': parser.get('InfluxDB', 'Host') or '127.0.0.1',
            'port': parser.get('InfluxDB', 'Port') or 8086,
            'database': parser.get('InfluxDB', 'Database') or None,

            # Get authentication info
            'user': parser.get('InfluxDB', 'User') or None,
            'pass': parser.get('InfluxDB', 'Pass') or None
        };

        # Configuration options for controlling collection and the daemon
        self.sysmond = {
            'sleep': int(parser.get('sysmond', 'Sleep')) or 10,

            # Get hostname override (if set)
            'hostname': parser.get('sysmond', 'Hostname') or socket.gethostname(),

            'collectors': parser.get('sysmond', 'Collectors').split(',') or None,
            'custom_collectors': parser.get('sysmond', 'CustomCollectors').split(',') or []
        };

        # The hard minimum is a 2 second delay.
        if self.sysmond['sleep'] < 2:
            self.sysmond['sleep'] = 2;

        if self.sysmond['collectors'] is None:
            raise ArgumentException("A list of collectors MUST be provided.")

        if self.influxdb['user'] is None and self.influxdb['pass'] is None:
            raise ArgumentException("A username and password must be provided.")
