import os
import shlex
import readline
import warnings

from climb.config import load_config
from climb.exceptions import CLIException
from climb.paths import ROOT_PATH

warnings.simplefilter("ignore")


class Climb(object):
    _prompt = "[{path}]> "
    _running = False

    def __init__(self, name, args, commands, completer, prompt=None):
        self._name = name
        self._config = load_config(name)

        self._current_path = ROOT_PATH
        self._verbose = self._config.getboolean(name, 'verbose')
        self._history_file = os.path.expanduser(self._config[name].get('history', ''))

        self._args = args(self)
        self._commands = commands(self)
        self._completer = completer(self)

        if prompt is not None:
            self._prompt = prompt

    def run(self):
        """Loops and executes commands in interactive mode."""
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self._completer.complete)

        if self._history_file:
            # Ensure history file exists
            if not os.path.isfile(self._history_file):
                open(self._history_file, 'w').close()

            readline.read_history_file(self._history_file)

        self._running = True
        try:
            while self._running:
                try:
                    command = input(self._format_prompt())
                    if command:
                        result = self.execute(*shlex.split(command))
                        if result:
                            print(result)
                except CLIException as exc:
                    print(exc)
                except (KeyboardInterrupt, EOFError):
                    self._running = False
        finally:
            if self._history_file:
                readline.write_history_file(self._history_file)

    def _format_prompt(self):
        return self._prompt.format(path=self._current_path)

    def execute(self, *args):
        """Executes single command and returns result."""
        command, kwargs = self.parse(*args)
        return self._commands.execute(command, **kwargs)

    def parse(self, *args):
        parsed = self._args.parse(*args)

        kwargs = dict(parsed._get_kwargs())
        command = kwargs.pop('command')

        return command, kwargs

    def log(self, message, *args, **kwargs):
        if self._verbose:
            print(message.format(*args, **kwargs))

    def set_running(self, running):
        self._running = running

    def set_current_path(self, current_path):
        self._current_path = current_path

    @property
    def args(self):
        return self._args

    @property
    def config(self):
        return self._config

    @property
    def commands(self):
        return self._commands

    @property
    def current_path(self):
        return self._current_path
