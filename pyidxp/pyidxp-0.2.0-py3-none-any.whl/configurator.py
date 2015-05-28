from consul import Consul
from json import load as jsonload, loads as jsonloads
from time import sleep
from shutil import which


class Configurator(object):
    @staticmethod
    def configuration(key, config_file='config.json', retries=10,
                      sleep_timeout=2):
        if which('consul'):
            c = Consul()
            for _ in range(retries):
                try:
                    value = c.kv.get(key)[1]['Value'].decode()
                    config = jsonloads(value)
                    return config
                except:
                    sleep(sleep_timeout)
        return jsonload(open(config_file, 'r'))
