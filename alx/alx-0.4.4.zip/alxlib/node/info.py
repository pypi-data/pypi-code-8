__author__ = 'Alex Gomes'

import logging
import socket, requests, platform

logging.getLogger("requests").setLevel(logging.CRITICAL)


class Info():
    def get_ip(self):
        try:
            logging.debug("get_ip")
            import requests

            r = requests.get(r'http://jsonip.com')
            return format(r.json()['ip'])
        except:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("gmail.com", 80))
                s.close()
                return format(s.getsockname()[0])
            except:
                return "0.0.0.0"


    def get_ip_local(self):
        return  socket.getsocket.gethostbyname(socket.getfqdn())


    def get_all(self):
        try:
            d = {}
            d['hostname'] = platform.node()
            d['os'] = platform.system()
            d["osversion"] = platform.version()
            d["osrelease"] = platform.release()
            d["system"] = platform.machine()
            d["processor"] = platform.processor()
            d["ip"] = self.get_ip()

            return d

        except Exception as e:
            logging.critical("Info()->get_all()->{0}".format(e))
            return None
