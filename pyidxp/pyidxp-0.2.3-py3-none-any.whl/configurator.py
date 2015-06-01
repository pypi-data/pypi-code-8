from consul import Consul, ConsulException
from json import load as jsonload, loads as jsonloads
from shutil import which


def configuration(key, config_file='config.json'):
    if which('consul'):
        c = Consul()
        try:
            value = c.kv.get(key)[1]['Value'].decode()
            config = jsonloads(value)
            return config
        except ConsulException:
            print("==> Configurator: Couldn't get configuration from Consul, "
                  "reading from file")
    return jsonload(open(config_file, 'r'))
