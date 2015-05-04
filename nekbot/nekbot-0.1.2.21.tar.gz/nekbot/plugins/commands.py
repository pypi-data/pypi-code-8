from nekbot.core.commands import cmds, command
from nekbot.core.types.argparse import Text, SetBool

__author__ = 'nekmo'

@command('commands', search=Text, by_plugin=SetBool('-p'))
def commands(msg, search='', by_plugin=False):
    if search:
        response = ''
        results_cmd, results_doc = cmds.search(search)
        if results_cmd:
            response += '- Results in commands names: %s' % ', '.join(sorted(results_cmd))
        if results_cmd and results_doc:
            response += '\n'
        if results_cmd:
            response += '- Results in documentation: %s' % ', '.join(results_doc)
        return response
    return 'Available commands: %s. Tip!! Use <command> -h for help.' % ' '.join(sorted(cmds.keys()))

