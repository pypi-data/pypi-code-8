PLUGIN_AUTHOR_NAME = 'Your name'
PLUGIN_AUTHOR_EMAIL = 'your@email'
PLUGIN_AUTHOR_WEBSITE = 'https://yourwebsite'
HOOK_BEFORE_CREATE_PLUGIN = ''
HOOK_AFTER_CREATE_PLUGIN = ''

STORAGE_DIR = 'storage'

PERMISSIONS_TREE = {
    'root': ['admin'],
    'admin': ['execution'],
    'execution': []
}

PROTOCOLS = [
]

PLUGINS = [
    'bot',
    'hello',
]

PERMS_METHODS = [
    'nekbot.core.permissions.perms_from_settings',
]

SYMBOL = '!'