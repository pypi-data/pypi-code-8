from checker import Checker
from collections import defaultdict
from styles import BOLD, DIM, ENDC, FAIL, OKBLUE


class CheckerResults(object):
    def __init__(self):
        self.checkers = []

    def __str__(self):
        mess = defaultdict(str, {})
        checkers = [c for c in self.checkers if c.err_messages]
        for c in checkers:
            if not mess[c.file]:
                mess[c.file] += self.HEADER.format(c.file)
            mess[c.file] += "\n" + str(c)

        out = "\n\n".join(mess.values())
        out += self.DISABLED if self.disabled else ""
        return (
            "{0}\n\t\t---------------------------{1}"
            "{2}\n\t\t GIT PATROL IS WATCHING YOU{1}"
            "{0}\n\t\t---------------------------{1}"
            "\n\n{3}\n\n"
            "You can disable the checkers in the gitpatrol.toml file, or you\n"
            "can completely disable Git Patrol for this commit by running \n"
            "`git commit --no-verify`.\n\n"
        ).format(FAIL, ENDC, OKBLUE, out)

    @property
    def has_errors(self):
        self._has_errors = any(map(lambda c: c.has_errors, self.checkers))
        return self._has_errors

    @has_errors.setter
    def has_errors(self, value):
        pass

    @property
    def disabled(self):
        self._disabled = not filter(lambda c: c.enabled, self.checkers)
        return self._disabled

    @disabled.setter
    def disabled(self, value):
        pass

    def record(self, checker):
        if isinstance(checker, Checker) and checker not in self.checkers:
            self.checkers.append(checker)

    HEADER = "{0}****{1} {2}{3}{1} {0}****{1}".format(FAIL, ENDC, BOLD, "{}")
    HELPFUL = """\n\n{0}Helpful Hints:{1}

\tgitpatrol enable {{checkername}}
\tgitpatrol disable {{checkername}}
\tgitpatrol tempenable {{checkername}}
\tgitpatrol tempdisable {{checkername}}

The relevant {{checkername}} appears in parentheses
following each error message.

You can also use flags like `-e`, `-d`, `-te`, or `-td`.
Run gitpatrol -d helpfulhints to disable this message.
""".format(BOLD, ENDC)
    DISABLED = (
        "No files were checked.\nEither no gitpatrol.toml config "
        "file was specified,\n or none of the checkers were enabled.")
