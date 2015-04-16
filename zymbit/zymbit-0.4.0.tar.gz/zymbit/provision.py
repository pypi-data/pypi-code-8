import logging
import shutil

from zymbit.compat import config, provision
from zymbit.util import get_system


class Provision(object):
    def __init__(self, token, api_url=None, websocket_url=None):
        self.token = token
        self.api_url = api_url
        self.websocket_url = websocket_url
        self.ssh_pubkey = None

    @property
    def logger(self):
        return logging.getLogger(__name__)

    def copy_files(self):
        files_root = config.FILES_ROOT
        if not files_root:
            self.logger.warning('files_root not defined, skipping copy_files')
            return

        self.logger.info('copying files from files_root={} to /'.format(files_root))

        try:
            _makedirs = shutil.os.makedirs
            shutil.os.makedirs = lambda *args, **kwargs: None
            shutil.copytree(files_root, '/')
        finally:
            shutil.os.makedirs = _makedirs

    def run(self):
        self.write_config()
        self.copy_files()

        system = get_system()

        try:
            provision.enable_init_script()
        except AttributeError:
            self.logger.warning('enable_init_script not found for system={}'.format(system))

        try:
            provision.start_service()
        except AttributeError:
            self.logger.warning('start_service not found for system={}'.format(system))

    def write_config(self):
        _config = config.get_config()

        if self.websocket_url:
            _config.setdefault('cloud', {})['websocket_url'] = self.websocket_url

        if self.api_url:
            _config.setdefault('cloud', {})['api_url'] = self.api_url

        _config.setdefault('auth', {})['provisioning_token'] = self.token

        config.save_config(_config)
