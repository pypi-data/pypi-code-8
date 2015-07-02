import configparser2
import os
import sys
import psutil

import console

class Utils:

    def __init__(self):
        self.DISK_SECTION = "DISK"
        self.INET_SECTION = "NET_INTERFACE"
        self.GENERAL_SECTION = "GENERAL"
        self.ENABLED = "enabled"

    def get_app_dir(self):
        if not os.path.exists(os.path.join(os.path.expanduser('~'), '.guardiancl/')):
            os.makedirs(os.path.join(os.path.expanduser('~'), '.guardiancl/'))
        return os.path.join(os.path.expanduser('~'), '.guardiancl/')

    def get_file(self, file):
        return os.path.join(self.get_app_dir() + file)

    def get_system_config(self):
        config = configparser2.ConfigParser()
        config.read(self.get_file(".guardiancl.ini"))
        dict_config = dict(config._sections)
        for key in dict_config:
            dict_config[key] = dict(config._defaults, **dict_config[key])
            dict_config[key].pop('__name__', None)
        return dict_config

    def get_config(self):
        if self._config_exist():
            config = configparser2.ConfigParser(delimiters=('='))
            config.read(self.get_file(".config.cfg"))
            dict_config = dict(config._sections)
            for key in dict_config:
                dict_config[key] = dict(config._defaults, **dict_config[key])
                dict_config[key].pop('__name__', None)
            return dict_config
        else:
            console.warn("Config file not found...")
            sys.exit(2)

    def _config_exist(self):
        return os.path.exists(self.get_file(".config.cfg"))

    def create_config_file(self, configs):
        config = configparser2.ConfigParser(delimiters=('='))
        config.add_section(self.DISK_SECTION)
        for key in configs['disks'].keys():
            config.set(self.DISK_SECTION, key, configs['disks'][key])

        config.add_section(self.INET_SECTION)
        for key in configs['net'].keys():
            config.set(self.INET_SECTION, key, configs['net'][key])

        config.add_section(self.GENERAL_SECTION)
        for key in configs['general'].keys():
            config.set(self.GENERAL_SECTION, key, configs['general'][key])

        with open(self.get_file(".config.cfg"), 'w') as configfile:
            config.write(configfile)

    def create_pid_file(self):
        pid = str(os.getpid())
        pid_file = self.get_file("guardiancl.pid")
        if os.path.exists(pid_file):
            pid_old = int(open(pid_file).read())
            if psutil.pid_exists(pid_old):
                console.error("Script already running!", True)
                sys.exit(2)
            else:
                target = open(pid_file, 'w')
                target.write(pid)
        else:
            target = open(pid_file, 'w')
            target.write(pid)

    def remove_pid_file(self):
        os.unlink(self.get_file("guardiancl.pid"))

    def alter_config_file(self, configs):
        config = configparser2.ConfigParser(delimiters=('='))
        config.read(self.get_file(".config.cfg"))

        if 'general' in configs:
            for key in configs['general'].keys():
                config.set(self.GENERAL_SECTION, key, configs['general'][key])
        if 'disk' in configs:
            for key in configs['disk'].keys():
                config.set(self.DISK_SECTION, key, configs['disk'][key])
        if 'inet' in configs:
            for key in configs['inet'].keys():
                config.set(self.INET_SECTION, key, configs['inet'][key])

        with open(self.get_file(".config.cfg"), 'w') as configfile:
            config.write(configfile)
