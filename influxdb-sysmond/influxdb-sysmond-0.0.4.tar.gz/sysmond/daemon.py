ascii = """
  .d8888. db    db .d8888. .88b  d88.  .d88b.  d8b   db d8888b.
  88'  YP `8b  d8' 88'  YP 88'YbdP`88 .8P  Y8. 888o  88 88  `8D
  `8bo.    `8bd8'  `8bo.   88  88  88 88    88 88V8o 88 88   88
    `Y8b.    88      `Y8b. 88  88  88 88    88 88 V8o88 88   88
  db   8D    88    db   8D 88  88  88 `8b  d8' 88  V888 88  .8D
  `8888Y'    YP    `8888Y' YP  YP  YP  `Y88P'  VP   V8P Y8888D'

       [ https://github.com/EvanDarwin/InfluxDB-sysmond/ ]
"""

from . import Config, WorkerManager

# Load default and custom collectors
import collectors, custom

import sys, time, json
import inspect, logging
import threading, socket

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(name)-8s] %(message)s',
                    datefmt='[%Y-%m-%d %H:%M]',
                    )

class Daemon(object):
    """ Handles all collectors and sending of data """

    def __init__(self, config):
        """ Creates a new daemon """

        self.config = config

        if config.influxdb['version'] is '0.9':
            from influxdb import InfluxDBClient
        else:
            from influxdb.influxdb08 import InfluxDBClient

        # Initialize important things
        self.client = InfluxDBClient(config.influxdb['host'],
                                     config.influxdb['port'],
                                     config.influxdb['user'],
                                     config.influxdb['pass'],
                                     config.influxdb['database'])

        self.logger = logging.getLogger('Daemon');
        self.manager = WorkerManager(config)

        print(ascii) # Happy server is happy.

        # Check that the Config is the correct type
        if not isinstance(config, Config):
            raise TypeError(
                "Configuration must of type DaemonConfig, is " + type(config).__name__
            );

        # Print the current configuration info (and hide the password)
        self.logger.info("Endpoint set at http://{}@***:{}:{}/db/{}".format(
            config.influxdb['user'],
            config.influxdb['host'],
            config.influxdb['port'],
            config.influxdb['database']
        ))

        # Print out an override notice if we're setting the hostname
        if config.sysmond['hostname'] is not socket.gethostname():
            self.logger.info('Hostname has been overridden to be \'{}\''.format(
                config.sysmond['hostname']
            ))

        self.register_collectors()
        self.collect()

    def register_collectors(self):
        # Register built-in collectors
        for name, obj in inspect.getmembers(collectors):
            if inspect.isclass(obj) and name is not 'CollectorThread':
                if obj.identifier: name = obj.identifier

                self.logger.debug('[+] Registering collector \'{}\''.format(name))
                self.manager.add(name, obj().run)

        # Register custom collectors
        #
        # TODO: Remove duplicate code
        for name, obj in inspect.getmembers(custom):
            if inspect.isclass(obj) and name is not 'CollectorThread':
                if obj.identifier: name = obj.identifier

                self.logger.debug('[+] Registering custom collector \'{}\''.format(name))
                self.manager.add(name, obj().run)

    def collect(self):
        self.logger.debug("Starting collector")

        while True:
            try:
                data = self.manager.collect_all()

                # Handle sending in its own thread.
                threading.Thread(target=self.send_metrics, args=([data])).run()

                # Wait before collecting again
                time.sleep(self.config.sysmond['sleep'])
            except KeyboardInterrupt:
                print("\n") # Print it so it doesn't push the line to the right
                self.logger.info("CTRL-C pressed, shutting down...")

                sys.exit(0)

    def send_metrics(self, data):
        self.client.write_points(data, time_precision='ms')
