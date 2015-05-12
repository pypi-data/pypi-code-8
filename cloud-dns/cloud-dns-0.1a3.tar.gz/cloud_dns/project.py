
import logging
import os.path as osp
import sys
import yaml

from libcloud.compute import providers

class Project(object):
    """Proxy around Apache LibCloud provider

    """
    def __init__(self, name, email_account, provider=None, pem_file=None):
        """
        :param name: Cloud project name
        :param email_account: service account name having proper permissions
        :param pem_file: absolute path to JSON key
        """
        driver = providers.get_driver(provider)
        logging.info("Creating driver over {} {} project".format(provider, name))
        self.driver = driver(
            email_account,
            pem_file,
            project=name
        )
        self.provider = provider

    def get_hostip_tuples(self):
        logging.info("Retrieving {} {} nodes".format(self.provider, self.driver.project))
        for node in self.driver.list_nodes():
            if any(node.public_ips):
                yield ("{}.{}".format(node.name,
                    self.driver.project), node.public_ips[0])
