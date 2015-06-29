import getpass
import json
import os
import platform
from datetime import datetime

import urllib3
import psutil
from apscheduler.schedulers.blocking import BlockingScheduler

import console
from utils import Utils
from account import Account
from device import Device

utils = Utils()
system_config = utils.get_system_config()
sched = BlockingScheduler()

def authenticate():
    serial = raw_input("Serial:")
    email = raw_input("E-mail:")
    password = getpass.getpass("Password:")

    if not serial or not email or not password:
        console.info("Serial, E-mail or Password Invalid!")
    else:
        http = urllib3.PoolManager()
        url = system_config['ROUTES'].get('auth')
        params = {'email': email, 'password': password}
        account = Account
        response = {}

        try:
            response = http.request('POST', url, params, encode_multipart=False)
        except Exception, e:
            console.error("Check your connection", exc_info=True)
            return None

        if response.status == 200:
            data = json.loads(response.data)
            return {'serial': serial, 'account': account(data['email'], response.getheaders()['user-key'], data['apiKey'])}
        else:
            console.error(response.data, True)
            return None

def create_config_file():
    account = authenticate()
    if account:
        device = None
        console.info("Checking device...")
        for dev in get_devices(account.get('account')):
            if dev.serial == account.get('serial'):
                device = dev
        console.info("Creating config file...")
        generate_config_file(account.get('account'), device)

def list_configs(opt):
    config = utils.get_config()

    def to_str(value, key):
        return "[%s] %s %s" % (value, "-", key)

    if opt == 'disk':
        disks = config[utils.DISK_SECTION]
        console.info('Disks list...', True)
        console.log('\n'.join([to_str(value, key) for key, value in disks.iteritems()]))
    if opt == 'inet':
        inet = config[utils.INET_SECTION]
        console.info('Net Interface list...', True)
        console.log('\n'.join([to_str(value, key) for key, value in inet.iteritems()]))

def start_monitor():
    console.info("Starting guardiancl monitor...", True)
    http = urllib3.PoolManager()
    utils.create_pid_file()

    def collect_job():
        config = utils.get_config()
        disks = config[utils.DISK_SECTION]
        interfaces = config[utils.INET_SECTION]
        account = Account(config[utils.GENERAL_SECTION].get('email'),
                          config[utils.GENERAL_SECTION].get('user_key'),
                          config[utils.GENERAL_SECTION].get('api_key'))

        report = {}
        usage = {}
        net = {}

        if os.name == 'nt':
            report['os'] = platform.system()+"-"+platform.win32_ver()[0]+" "+platform.win32_ver()[2]
            report['arch'] = platform.architecture()[0]
        else:
            report['loadAverage'] = {}
            if not os.name == 'nt':
                for idx, la in enumerate(os.getloadavg()):
                    time_la = "1" if idx == 0 else "5" if idx == 2 else "15"
                    report['loadAverage'][time_la] = "{0:.2f}".format(la)
            if platform.system() == 'Linux':
                report['os'] = platform.linux_distribution()[0]+"-"+platform.linux_distribution()[1]+" "+platform.linux_distribution()[2]
                report['arch'] = platform.architecture()[0]
            else:
                report['os'] = "Mac OS X - "+platform.mac_ver()[0]
                report['arch'] = platform.architecture()[0]

        for disk in disks.keys():
            if disks[disk] == utils.ENABLED:
                usage_temp = psutil.disk_usage(disk)
                usage[disk] = {'total': usage_temp.total, 'used': usage_temp.used, 'free': usage_temp.free,
                               'percentage': usage_temp.percent}
        for interf in interfaces.keys():
                if interfaces[interf] == utils.ENABLED:
                    net_temp = dict((k.lower(),v) for k, v in psutil.net_io_counters(pernic=True).iteritems())[interf]
                    net[interf] = {'sent': net_temp.bytes_sent, 'recv': net_temp.bytes_recv}
        report['inet'] = net
        report['disks'] = usage
        report['processes'] = {'value': len(psutil.pids())}

        report['loadAverage'] = {}
        if not os.name == 'nt':
            for idx, la in enumerate(os.getloadavg()):
                time_la = "1" if idx == 0 else "5" if idx == 2 else "15"
                report['loadAverage'][time_la] = "{0:.2f}".format(la)
        report['users'] = {'value': len(psutil.users())}
        report['uptime'] = str(datetime.now() - datetime.fromtimestamp(psutil.boot_time())).split('.')[0]
        report['kindDevice'] = 3

        api_key = account.api_key
        url = "%s/%s" % (system_config['ROUTES'].get('collect'), config[utils.GENERAL_SECTION].get('serial'))

        params = {'apiKey': api_key, 'data': json.dumps(report)}

        try:
            response = http.request('POST', url, params, {'user-key': account.user_key}, encode_multipart=False)
        except Exception, e:
            console.error("Check your connection")
            return

        if response.status == 200:
            console.info("Information sent...")
        else:
            data = json.loads(response.data)
            console.error(data['status'])

    console.info("Sending informations...")
    sched.add_job(collect_job, 'interval', max_instances=1, seconds=5)

    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        utils.remove_pid_file()
        pass

def get_devices(account):
    http = urllib3.PoolManager()
    url = system_config['ROUTES'].get('devices')

    if account is not None:
        try:
            response = http.request('GET', url, None, {'user-key': account.user_key})
        except Exception, e:
            console.error("Check your connection", exc_info=True)

        if response.status == 200:
            devices = []
            for dev in json.loads(response.data):
                devices.append(Device(dev['serial'], dev['description']))
            return devices
        else:
            data = json.loads(response.data)
            console.error(data['status'])
            return None

def generate_config_file(account, device):
    if account is not None and device is not None:
        disks_temp = []
        for part in psutil.disk_partitions(all=False):
                disks_temp.append(part.mountpoint)
        disks = dict([(disk, "enabled") for idx, disk in enumerate(disks_temp)])
        net = dict([(net, "enabled") for idx, net in
                        enumerate(psutil.net_io_counters(pernic=True).keys())])
        general = {'email': account.email, 'user_key': account.user_key, 'serial': device.serial,
                       'api_key': account.api_key}
        configs = {'disks': disks, 'net': net, 'general': general}
        utils.create_config_file(configs)
        console.info("Config file created...")
    else:
        console.info("Account or Device not found...")


def update_config_file(type_conf=utils.GENERAL_SECTION):
    config = utils.get_config()
    if type_conf == utils.GENERAL_SECTION:
        serial_conf = config[utils.GENERAL_SECTION].get('serial')
        user_key_conf = config[utils.GENERAL_SECTION].get('user_key')
        api_key_conf = config[utils.GENERAL_SECTION].get('api_key')
        email_conf = config[utils.GENERAL_SECTION].get('email')

        serial = raw_input("Serial  [%s]: " % serial_conf) or serial_conf
        user_key = raw_input("UserKey [%s]: " % user_key_conf) or user_key_conf
        api_key = raw_input("ApiKey  [%s]: " % api_key_conf) or api_key_conf
        email = raw_input("Email   [%s]: " % email_conf) or email_conf

        utils.alter_config_file({'general': {'serial': serial, 'user_key': user_key,
                                             'api_key': api_key, 'email': email}})
        console.info("New config saved...")
    elif type_conf == utils.DISK_SECTION:
        new_config = {'disk': {}}
        console.log("Type: y - 'enable' or n - 'disabled'")
        disks = config[utils.DISK_SECTION]
        for disk, value in disks.iteritems():
            diskValue = raw_input("%s  [%s]: " % (disk, value)) or value
            if diskValue in ['y', 'yes']:
                diskValue = 'enabled'
            elif diskValue in ['n', 'no']:
                diskValue = 'disabled'

            new_config['disk'][disk] = diskValue
        utils.alter_config_file(new_config)
        console.info("New config saved...")
    elif type_conf == utils.INET_SECTION:
        new_config = {'inet': {}}
        console.log("Type: y - 'enable' or n - 'disabled'")
        inets = config[utils.INET_SECTION]
        for inet, value in inets.iteritems():
            inetValue = raw_input("%s  [%s]: " % (inet, value)) or value
            if inetValue in ['y', 'yes']:
                inetValue = 'enabled'
            elif inetValue in ['n', 'no']:
                inetValue = 'disabled'

            new_config['inet'][inet] = inetValue
        utils.alter_config_file(new_config)
        console.info("New config saved...")
