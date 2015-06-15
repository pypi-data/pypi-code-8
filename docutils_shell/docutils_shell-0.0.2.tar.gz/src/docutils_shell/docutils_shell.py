"""
Invoke each shell directive once to retrieve and store its data.
Each command is run in its own shell from the project's base directory.
Use the appropriate (replacement) tag to display the stored data.

For example, this markup::

    .. shell:: hg parent --template {rev}
               REVISION

    .. shell:: date "+built on %a %d %b %Y at %X %Z"
               TIMESTAMP

    Revision |REVISION|, |TIMESTAMP|

Will appear something like this::

    Revision 5, built on Sun 14 Jun 2015 at 13:02:21 CDT

"""
from docutils import statemachine
from docutils.parsers import rst
import subprocess
import time

SETTINGS = {
        'project_base':     '.',
        }

class ShellDirective(rst.Directive):
    """ShellDirective::
    
        .. shell:: cmd
                   tag

    Runs `cmd` in its own shell 
    from the base of the project (SETTINGS['project_base']),
    and places the standard output into `tag`.
    Use ``|tag|`` to retrieve the output.
    """
    required_arguments = 2
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}
    has_content = False

    def convert_to_rst(self, data):
        return '.. |%s| replace:: %s\n\n' % (self.tag, data)

    def get_data(self):
        return subprocess.check_output(
                self.cmd, 
                cwd=SETTINGS['project_base'],
                shell=True)

    def insert(self, rst):
        tab_size = 4
        include_lines = statemachine.string2lines(
                rst,
                tab_size,
                convert_whitespace=True)
        self.state_machine.insert_input(include_lines, '')
        return []

    def run(self):
        args = ' '.join(self.arguments).split()
        self.cmd = ' '.join(args[:-1])
        self.tag = args[-1]
        return self.insert(self.convert_to_rst(self.get_data()))

rst.directives.register_directive('shell', ShellDirective)

