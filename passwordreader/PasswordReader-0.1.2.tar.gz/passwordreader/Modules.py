import os
import getpass
import PasswordReader
from sys import argv

__all__ = ["PasswordReaderModule",
           "EnvironmentModule",
           "FileModule",
           "ConsoleModule"]


class EnvironmentModule(PasswordReader.PasswordReaderModule):

    def __init__(self, variable_name):
        self._variable_name = variable_name

    def readPassword(self):
        if self._variable_name in os.environ:
            return os.environ[self._variable_name]
        else:
            return None


class FileModule(PasswordReader.PasswordReaderModule):

    def __init__(self, file_name):
        self._file_name = file_name

    def readPassword(self):
        file_name = self._file_name

        if file_name.startswith('@'):
            file_name = os.path.join(
                os.path.dirname(os.path.realpath(argv[0])), file_name[1:])

        try:
            with open(file_name) as f:
                return f.readline()
        except IOError:
            return None


class ConsoleModule(PasswordReader.PasswordReaderModule):

    def __init__(self, prompt):
        self._prompt = prompt

    def readPassword(self):
        return getpass.getpass(self._prompt)


class ValueModule(PasswordReader.PasswordReaderModule):

    def __init__(self, value):
        self._value = value

    def readPassword(self):
        return self._value
