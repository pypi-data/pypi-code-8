import json
import os

API_URL = os.environ.get('API_URL', 'https://zymbit.com/api/v1')
CONFIG_PATH = os.environ.get('CONFIG_PATH', '/etc/zymbit.conf')
PROVISION_PATH = os.environ.get('PROVISION_PATH', '/provision')

TUNNEL_SSH_KEY_PATH = os.path.expanduser(os.environ.get('TUNNEL_SSH_KEY_PATH', '~/.ssh/id_tunnel'))

INIT_SCRIPT_PATH = '/etc/init.d/zymbit'
FILES_ROOT = None


def get_config():
    if os.path.exists(CONFIG_PATH):
        return json.load(open(CONFIG_PATH, 'rb'))

    return {}


def save_config(config):
    json.dump(config, open(CONFIG_PATH, 'wb'))
