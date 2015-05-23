import readline


class Completer(object):

    def __init__(self, cli):
        self._cli = cli
        self._completions = {}

    def complete(self, text, state):
        buffer = readline.get_line_buffer()

        if ' ' in buffer.lstrip():
            command, kwargs = self._cli.parse(*buffer.split())

            method = self._completions.get(command, self._default_completer())
            completions = method(**kwargs)
        else:
            completions = [command.name for command in self._cli.args.commands]

        completions = [c for c in completions
                       if c.startswith(text)]

        if state < len(completions):
            return completions[state]
        else:
            return None

    def _default_completer(self):
        raise NotImplemented("Default completer not set")
