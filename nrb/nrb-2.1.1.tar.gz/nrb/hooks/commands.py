__author__ = 'Hi'

from nrb.hooks import base


class CommandsConfig(base.BaseConfig):

    section = 'global'

    def __init__(self, config):
        super(CommandsConfig, self).__init__(config)
        self.commands = self.config.get('commands', "")
        print "[pbr.hooks.commands.CommandsConfig]: ", self.commands
        print "\n"

    def save(self):
        self.config['commands'] = self.commands
        print "[pbr.hooks.commands.CommandsConfig.self.config['commands']]: ", self.config['commands']
        super(CommandsConfig, self).save()

    def add_command(self, command):
        print "pbr.hooks.commands.add_command: ENTERED."
        self.commands = "%s\n%s" % (self.commands, command)
        print "pbr.hooks.commands.add_command.self.commands: ", self.commands
        print "pbr.hooks.commands.add_command: CLOSED."
        print "\n"

    def hook(self):
        print "pbr.hooks.commands.hook: ENTERED"
        self.add_command('nrb.packaging.LocalEggInfo')
        self.add_command('nrb.packaging.LocalSDist')
        self.add_command('nrb.packaging.LocalInstallScripts')
        print "pbr.hooks.commands.hook: CLOSED"
        print "\n"
