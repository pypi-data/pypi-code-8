
from pipeline.command import (
    BakedCommand,
    register_baked_command_task,
)




class ProspectorCommand(BakedCommand):
    """
    Command subclass for installing and running prospector command.
    """
    __id = 'prospector'
    install = ['pip2', 'install', '--upgrade', 'prospector']


    def instructions(self):

        return [[
            'prospector',
        ]]


register_baked_command_task('prospector', workspace_class='python_workspace')