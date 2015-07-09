
import re

from pipeline.command import (
    BakedCommand,
    register_baked_command_task,
)


class CoverageDiffCommand(BakedCommand):
    """
    Command subclass for installing and running flake8-diff command.
    """
    __id = 'coverage_diff'
    install = ['pip', 'install', '--upgrade', 'diff_cover']

    def instructions(self):
        """Return subprocess cmd for execution.
        :returns: subprocess-friendly list to run diff_cover

        Expects self.source to have an 'output' that will contain coverage xml.
        Quack like a duck.
        """
        return [
            'http_proxy= curl {} --user {}:{} -o  coverage.xml'.format(
                self.retval.url,
                self.retval.user,
                self.retval.passwd
            ),
            [
            'diff-cover',
            'coverage.xml',
            '--compare-branch=origin/{}'.format(self.source.dest_branch),
            ]
        ]


register_baked_command_task('coverage_diff', workspace_class='python_workspace')

