import ConfigParser

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