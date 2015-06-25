def make_wsgi_app(global_config, **kw):
    settings = kw.get('settings')
    if settings is None:
        raise ValueError('Must provide "settings" value')

    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = settings
    try:
        from django.core.wsgi import get_wsgi_application
        return get_wsgi_application()
    except ImportError:
        from django.core.handlers.wsgi import WSGIHandler
        return WSGIHandler()
