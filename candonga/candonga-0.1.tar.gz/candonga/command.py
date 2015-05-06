import logging

from cliff.command import Command


class CreateProject(Command):
    "Create an empty project."

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.debug('debugging')
        self.app.stdout.write('project created!\n')

class CreateInfraProject(Command):
    "Create an deploy empty project."

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.debug('debugging')
        self.app.stdout.write('project created!\n')

