import os
###import logging
#from tg import config

import pyramid


#log = logging.getLogger ('bq.util.paths')
def getsettings(**kw):
    settings = kw.get ('settings')
    if settings is None:
        registry = pyramid.threadlocal.get_current_registry()
        settings = registry.settings
        #log.warn ('SETTINGS %s' , settings)

    return settings


def bisque_root(**kw):
    root = os.environ.get('BISQUE_ROOT')
    settings = getsettings(**kw)
    return (root or settings.get('bisque.paths.root') or '').replace('\\', '/')

def bisque_path(*names, **kw):
    'return a path constructed from the installation path'
    root = bisque_root(**kw)
    return os.path.join(root, *names).replace('\\', '/')

def data_path(*names, **kw):
    'return a path constructed from the data directory path'
    settings = getsettings(**kw)
    data = settings and settings.get('bisque.paths.data')
    data = data or os.path.join(bisque_root(**kw), 'data')
    return os.path.join(data, *names).replace('\\', '/')


def config_path(*names, **kw):
    'return a path constructed from the config directory path'
    settings = getsettings(**kw)
    conf = settings and settings.get('bisque.paths.config')
    conf = conf or os.path.join(bisque_root(**kw), 'config')
    return os.path.join(conf, *names).replace('\\', '/')


def site_cfg_path(**kw):
    'find a site.cfg from the usual places: locally, config, or /etc'
    settings = getsettings(**kw)
    site_cfg = settings and settings.get('bisque.paths.site_cfg')
    if site_cfg is not None:
        return site_cfg.replace('\\', '/')
    paths = ['.', 'config', '/etc/bisque']
    for d in paths:
        site_cfg = os.path.join(d, 'site.cfg')
        if os.path.exists(site_cfg):
            return site_cfg.replace('\\', '/')
    return None


