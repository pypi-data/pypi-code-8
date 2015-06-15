__author__ = 'Hi'
class BaseConfig(object):

    section = None

    def __init__(self, config):
        print "\n"
        self._global_config = config
        print "[base.BaseConfig.__init__.self._global_config]: ", self._global_config
        print "\n"
        self.config = self._global_config.get(self.section, dict())
        print "base.BaseConfig.__init__.self.section: ", self.section
        print "\n"
        print "[base.BaseConfig.__init__.self.config]: ", self.config
        self.pbr_config = config.get('nrb', dict())
        print "\n"
        print "[base.BaseConfig.__init__.self.pbr_config]: ", self.pbr_config

    def run(self):
        print "self: ", self
        self.hook()
        self.save()
        print "\n"

    def hook(self):
        pass

    def save(self):
        print "The program has entered into the base save method. "
        self._global_config[self.section] = self.config
        print "[pbr.base.BaseConfig.self._global_config[self.section]]: ", self._global_config[self.section]