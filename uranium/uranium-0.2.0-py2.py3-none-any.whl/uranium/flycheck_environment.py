import os


class Environment(dict):
    """
    a uranium interface exposed which allows the setting of
    environment variables
    """

    def __setitem__(self, key, item):
        super(Environment, self).__setitem__(key, item)
        os.environ[key] = item

    def generate_injection(self):
        """ generate the injection necessary to recreate th