import importlib
#from django.utils.module_loading import import_module


def get_urlconf(plugin_name, frontend_urls=True):
    plugin_settings = importlib.import_module(plugin_name + '.plugin')
    uconf_type = 'FRONTEND_URLCONF' if frontend_urls else 'BACKEND_URLCONF'
    urlconf = getattr(plugin_settings, uconf_type)
    return urlconf