
import os.path as osp
import sys
import yaml

from libcloud.compute import providers

DEFAULT_YAML_CONFIG = osp.expanduser('~/.config/cloud-dns/projects.yml')

def load_file(input_file):
    with open(input_file) as istr:
        return yaml.load(istr)

def load_from_file(input_file):
    for project, settings in load_file(input_file).items():
        yield get_driver(project, **settings)

def get_driver(project=None, email_account=None, provider=None, pem_file=None):
    driver = providers.get_driver(provider)
    print 'building project %s' % project
    return driver(
        email_account,
        pem_file,
        project=project
    )

def get_hostip_tuples(drivers):
    for driver in drivers:
        for node in driver.list_nodes():
            if any(node.public_ips):
                yield ("{}.{}".format(node.name, node.driver.project), node.public_ips[0])

def update_etc_hosts(hostip_tuples):
    BEGIN_MARKUP = '# CloudDNS prelude - DO NOT REMOVE\n'
    END_MARKUP = '# CloudDNS epilogue - DO NOT REMOVE\n'
    with open('/etc/hosts', 'r+') as etc_hosts:
        lines  = etc_hosts.readlines()
        etc_hosts.seek(0)
        etc_hosts.truncate(0)
        previous_content_replaced = False
        between_markups = False
        for line in lines:
            if not between_markups:
                if line == BEGIN_MARKUP:
                    between_markups = True
                etc_hosts.write(line)
            else:
                if line == END_MARKUP:
                    previous_content_replaced = True
                    for host, ip in hostip_tuples:
                        etc_hosts.write("{:>16} {}\n".format(ip, host))
                    between_markups = False
                    etc_hosts.write(line)
        if not previous_content_replaced:
            etc_hosts.write(BEGIN_MARKUP)
            for host, ip in hostip_tuples:
                etc_hosts.write("{} {}\n".format(ip, host))
            etc_hosts.write(END_MARKUP)

def run():
    if len(sys.argv) > 1:
        config = sys.argv[1]
    else:
        config = DEFAULT_YAML_CONFIG
    hostip_list = list(get_hostip_tuples(load_from_file(config)))
    update_etc_hosts(hostip_list)

if __name__ == '__main__':
    run()
