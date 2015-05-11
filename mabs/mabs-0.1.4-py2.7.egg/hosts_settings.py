#!/usr/bin/env  python
#coding:utf-8


import ConfigParser
import sys
import re

class HostSearch(object):
    """
    control the group clients or single client
    """

    def __init__(self):
        self.config = ConfigParser.ConfigParser(allow_no_value=True)
        self.config.optionxform = str
        self.secret = ConfigParser.ConfigParser(allow_no_value=True)
        self.secret.optionxform = str
        try:
            self.config.read('/etc/ansible/hosts')
            self.secret.read('/etc/ansible/secret.ini')
        except ConfigParser.ParsingError, e:
            print e
            sys.exit(2)
        #self.hosts = ''

    def tidy_parse(self, hostlists):
        """
        determine whether is single or group clients
        """
        if len(hostlists.split(',')) == 1:
            hosts = self.init_parse(hostlists)
        else:
            hosts = '\n'.join([self.init_parse(i) for i in hostlists.split(',')])
        return hosts

    def show(self, hostlists):
        print self.tidy_parse(hostlists)

    def single_host_dict(self, conf, origin_conf):
        hosts_para = [ origin_conf,
            self.secret.get(conf, 'port'),
            self.secret.get(conf, 'user'),
            self.secret.get(conf, 'password')]
        return hosts_para

    def search_hosts(self, host):
        with open('/etc/hosts', 'r') as f:
            hosts_txt = f.readlines()
        ip_compile = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        for i in hosts_txt:
            try:
                line = i.strip()
                if re.search(r'\b' + host + r'\b', line):
                    host_ip = ip_compile.search(line).group()
                    break
                else:
                    raise
            except:
                pass
        try:
            return host_ip
        except:
            return host

    def get_single_host(self, conf):
        origin_conf = self.search_hosts(conf)
        try:
            hosts_para = self.single_host_dict(conf, origin_conf)
        except:
            conf = 'default'
            hosts_para = self.single_host_dict(conf, origin_conf)
        single_host = ' '.join(hosts_para)
        return single_host

    def init_parse(self, hostlists):
        """
        form the all clients into a strings
        """
        hosts_setlist = []
        try:
            set_conf = [i for i in self.config.options(hostlists)]
            for i in set_conf:
                single_host = self.get_single_host(i)
                hosts_setlist.append(single_host)
                hosts_set = '\n'.join(hosts_setlist)
        except:
            hosts_set = self.get_single_host(hostlists)
        return hosts_set


if __name__ == '__main__':
    H = HostSearch()
    H.tidy_parse('group-name1')
    H.tidy_parse('web3')
    # H.show('group-name2')
    # H.show('web2')
