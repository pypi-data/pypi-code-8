from . import util
from flask import Flask
from os.path import expanduser
from werkzeug.exceptions import default_exceptions
import os


class Meh(object):
    def __init__(self, name=None, config={}):
        self._module = name.split('.')[-1]

        self.app = Flask(self._module)
        self.app.config.update(**config)

        self._load_config()
        self._configure_logging()


    def _load_config(self):
        """
        Override app.config from externalized config files. First checks the
        path provided by $PODHUB_MODULE_CONFIG_PATH envvar, then the user's
        config directory (~/.config/) then at the system level (/etc/).
        """
        env = os.getenv('PODHUB_{}_CONFIG_PATH'.format(self._module))
        home = expanduser(
            '~/.config/podhub/{}/config.py'.format(self._module))
        system = '/etc/podhub/{}/config.py'.format(self._module)

        for path in (env, home, system):
            if path and os.access(path, os.R_OK):
                self.app.config.from_pyffile(path, silent=True)
                break

    def _configure_logging(self):
        """
        Set up basic file logging.
        """
        if not self.app.debug:
            from logging import FileHandler
            import logging

            _log_path = '/var/log/podhub/{}/app.log'.format(self._module)
            file_handler = FileHandler(
                self.app.config.get('LOG_FILE', _log_path))
            file_handler.setLevel(
                getattr(logging, self.app.config.get('LOG_LEVEL', 'WARNING')))
            self.app.logger.addHandler(file_handler)

    def _log_errors(self):
        """
        Configure json-formatted error logging.
        """
        for code in default_exceptions.iterkeys():
            self.app.error_handler_spec[None][code] = util.make_json_error
