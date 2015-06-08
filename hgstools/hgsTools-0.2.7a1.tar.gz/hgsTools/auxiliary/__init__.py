import ConfigParser
import logging
import os
import netifaces as ni

def read_option(config, section, option):
    if not config.has_section(section):
        raise ConfigParser.ParsingError("Section %s not found" % section)
    if not config.has_option(section, option):
        raise ConfigParser.ParsingError("Section %s has no option %s" % (section, option))
    
    return config.get(section, option)

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

def buildRabbitMQConnectionLink(address, protocol='amqp', user='rabbitmq', password='rabbitmq', port='5672'):
    link = protocol + '://' + user + ':' + password + '@' + address + ':' + port + '//'
    
    return link

def getIPAdreess(interface='eth0'):
    addr = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    return addr

def initLogger(log_file, logging_level):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr = logging.FileHandler(log_file)
    hdlr.setFormatter(formatter)
    
    logger = logging.getLogger(__name__)
    logger.addHandler(hdlr) 
    logger.setLevel(logging_level)
    
    return logger

def make_dirs(path):
    try: 
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise