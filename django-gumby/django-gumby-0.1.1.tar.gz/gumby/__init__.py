__version__ = '0.1.1'


def autodiscover():
    """
    Auto-discover healthchecks health_check.py modules and fail silently when
    not present. This forces an import on them to register any healt checks bits
    they may want.
    """

    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule
    from gumby.healthchecks import healthchecks_dir

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's health_check module.
        try:
            before_import_registry = copy.copy(healthchecks_dir._registry)
            import_module('%s.health_check' % app)
        except:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            healthchecks_dir._registry = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have a health_check module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'health_check'):
                raise
