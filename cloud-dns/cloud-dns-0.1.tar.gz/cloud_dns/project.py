
import logging
import os.path as osp
import sys
import yaml

from libcloud.compute import providers

DEFAULT_HOST_ALIASES = ["{node_name}.{project_name}"]

class Project(object):
    """Proxy around Apache LibCloud provider

    """
    def __init__(self, name, email_account, provider=None, pem_file=None, aliases=None):
        """
        :param name: Cloud project name
        :param email_account: service account name having proper permissions
        :param pem_file: absolute path to JSON key
        :param aliases: list of additional aliases to create, for instance {node_name}.c.{project_name}.internal
        """
        driver = providers.get_driver(provider)
        logging.info("Creating driver over {} {} project".format(provider, name))
        self.driver = driver(
            email_account,
            pem_file,
            project=name
        )
        self.provider = provider
        self.aliases = aliases or DEFAULT_HOST_ALIASES

    def get_hostip_tuples(self):
        logging.info("Retrieving {} {} nodes".format(self.provider, self.driver.project))
        for node in self.driver.list_nodes():
            if any(node.public_ips):
                hosts = []
                for alias in self.aliases:
                    hosts.append(alias.format(**{
                        'node_name': node.name,
                        'project_name': self.driver.project
                        }))
                yield (tuple(hosts), node.public_ips[0])
