"""
Flake8Diff support

"""
import re

from pipeline.command import (
    BakedCommand,
    register_baked_command_task,
    LineOutputFormatter
)


class Flake8LintFormatter(LineOutputFormatter):
    """Format linter errors.
    Currently unused, fix is part of Milestone2
    (violation comment on individual commits instead of on pull request)
    """
    def __call__(self, output):
        """Return list-ified output."""
        file_re = re.compile(r'^Found violations: (?P<path>.*)$')
        violations = []
        _file = None
        for line in super(Flake8LintFormatter, self).__call__(output):
            match = file_re.match(line)
            if match:
                _file = match.group('path')
                continue
            elif line.startswith('\t'):
                violations.append((_file, line.strip()))
                continue

        return violations


class Flake8DiffCommand(BakedCommand):
    """
    Command subclass for installing and running flake8-diff command.
    """
    __id = 'flake8_diff'
    install = ['pip', 'install', '--upgrade', 'flake8-diff']
    # removed - will be resolved with "allow output transformation for actions"
    # formatter = Flake8LintFormatter

    def instructions(self):
        """Return subprocess cmd for execution.
        :returns: subprocess-friendly list to run flake8-diff

        Expects self.source to be a ``github3.pulls.pull_request`` instance.
        Quack like a duck.
        """
        return [[
            'flake8-diff',
            # will always be origin, since we initially cloned `base`
            'origin/{}'.format(self.context.source.dest_branch),
            #TODO implement configurable params for shell commands
            '--flake8-options', '--ignore=E501', '--exclude=\*_tables.py',
        ]]


register_baked_command_task('flake8_diff', workspace_class='python_workspace')

