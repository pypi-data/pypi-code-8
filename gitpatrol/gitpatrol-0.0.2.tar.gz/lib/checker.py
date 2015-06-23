import os
import re
from subprocess import check_output
from subprocess import CalledProcessError


class Checker(object):
    """There is nothing in here that a contributor would necessarily
    need to look at if they simply wanted to add an new checker.
    """

    def __init__(self, opts=None):
        # If no opts are provided in params, then assign empty dict
        opts = opts or {}

        # Set up all parameters based on opts
        self.file = opts.get("filepath", "")
        self.changed_code = opts.get("changes", "")
        self.hook_key = opts.get("key", "basechecker")
        self.forbidden = [re.compile(f) for f in opts.get("forbidden", [])]
        self.files_to_check = opts.get("check", [])
        self.files_to_ignore = opts.get("ignore", [])
        self._pref_override = opts.get("enabled", False)

    def __str__(self):
        return "\n".join(self.err_messages)

    @property
    def err_messages(self):
        self._err_messages = reduce(
            lambda a, m: a + [self.warning_message(m)],
            self.validate_changes(), [])
        return self._err_messages

    @err_messages.setter
    def err_messages(self, value):
        pass

    @property
    def has_errors(self):
        self._has_errors = bool(self.err_messages)
        return self._has_errors

    @has_errors.setter
    def has_errors(self, value):
        pass

    @property
    def enabled(self):
        cmd = "git config --get gitpatrol.{}".format(self.hook_key)
        try:
            self._enabled = check_output(cmd.split()).strip().lower() == "true"
            return self._enabled
        except CalledProcessError as e:
            self._enabled = bool(self._pref_override)
            return self._enabled

    @enabled.setter
    def enabled(self, value):
        pass

    @property
    def to_check(self):
        file_ext = os.path.splitext(self.file)[1]
        self._to_check = file_ext in self.files_to_check
        return self._to_check if self.files_to_check else True

    @to_check.setter
    def to_check(self, value):
        pass

    @property
    def to_ignore(self):
        file_ext = os.path.splitext(self.file)[1]
        self._to_ignore = file_ext in self.files_to_ignore
        return self._to_ignore

    @to_ignore.setter
    def to_ignore(self, value):
        pass

    def validate_changes(self):
        if not self.enabled:
            return []
        if not self.to_check or self.to_ignore:
            return []
        ms = map(lambda f: re.search(f, self.changed_code), self.forbidden)
        return [m.group() for m in filter(None, ms)]

    def warning_message(self, string):
        msg = "\"{}\" found, but not allowed ({})."
        return msg.format(string, self.hook_key)
