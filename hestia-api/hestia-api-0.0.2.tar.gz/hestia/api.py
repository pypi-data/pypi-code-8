import logging
import requests
import simplejson as json
import time
from six.moves.urllib.parse import urljoin
import six.moves.configparser as configparser
from sys import version_info


def load_configuration():
    config = configparser.ConfigParser()
    config_file = '/etc/hestia.conf'

    if version_info.major == 2:
        config.readfp(open(config_file))
    else:
        with open(config_file) as h:
            config.read_string(h.read())
    return config


class HestiaApi:
    def __init__(self, settings):
        self.__log = logging.getLogger("HestiaApi")
        self.__settings = settings

    def record_solar_river_reading(self, pv_output):
        payload = {
            "date": str(pv_output.date_taken),
            "temp": pv_output.internal_temperature.value,
            "vpv1": pv_output.panel1_voltage.value,
            "ipv1": pv_output.panel1_dc_current.value,
            "iac": pv_output.grid_current.value,
            "vac": pv_output.grid_voltage.value,
            "fac": pv_output.grid_frequency.value,
            "pac": pv_output.output_power.value,
            "htotal": pv_output.working_hours_total.value,
            "etoday": pv_output.accumulated_energy_today.value,
            "etotal": pv_output.accumulated_energy_total.value
        }

        self.__log.debug('Posting %s' % json.dumps(payload))
        self.__post(
            'photovoltaic/' + self.__settings.get('Photovoltaic',
                                                  'installation_code') + '/inverter/solar_river/readings',
            json.dumps(payload),
            {'content-type': 'application/json'})

    def record_emon(self, data):
        sent_at = int(time.time())
        data_string = json.dumps(data, separators=(',', ':'))
        payload = "data=" + data_string + "&sentat=" + str(sent_at)

        self.__post('property/' + self.__settings.get('Emon', 'property_code') + '/emon/readings', payload,
                    {'content-type': 'application/x-www-form-urlencoded'})

    def status(self):
        return self.__get('status', {'content-type': 'application/json'})

    def __post(self, path, payload, headers=None):
        if not headers:
            headers = {}
        url = self.__remote_url(path)

        self.__log.debug('Sending POST request to %s' % url)
        r = requests.post(url,
                          timeout=5,
                          data=payload,
                          headers=headers,
                          auth=self.__authentication())
        self.__log.debug('Received server response %s' % r.status_code)
        return r.status_code

    def __get(self, path, headers=None):
        if not headers:
            headers = {}
        url = self.__remote_url(path)

        self.__log.debug('Sending GET request to %s' % url)
        r = requests.get(url,
                         timeout=5,
                         headers=headers,
                         auth=self.__authentication())
        self.__log.debug('Received server response %s' % r.status_code)
        return r.status_code

    def __remote_url(self, path):
        return urljoin(self.__settings.get('Remote', 'url'), path)

    def __authentication(self):
        return self.__settings.get('Remote', 'username'), self.__settings.get('Remote', 'password')
