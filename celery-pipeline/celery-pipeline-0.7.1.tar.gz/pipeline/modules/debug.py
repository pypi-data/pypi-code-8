import time

from pipeline.actions import action, TaskResult
from pipeline.command import BakedCommand, register_baked_command_task

import logging
logger = logging.getLogger(__name__)

class EchoCommand(BakedCommand):
    """This command will echo whatever the
    souurce was."""
    __id = 'echo_test_command'
    def instructions(self):
        return [['echo', self.context.source]]

register_baked_command_task('echo_test_command')

class DummyFileSource(object):
    def __init__(self, filename, contents):
        self.acquisition_instructions = {
            'command': 'echo {} >> {}'.format(
                contents, filename
            )
        }
        
@action
def print_something(self, source, the_thing=None):

    logger.error('printing something')
    for i in range(3):
        logger.error('{} {}'.format(the_thing, i))
        time.sleep(0.5)
    logger.error('done printing something')

    return TaskResult(False, output=the_thing)

@action
def log_stuff(self, source):
    """Print some stuff to the console."""
    logger.error(source)



@action
def dummy_action(self, source, **kwargs):
    return 1

