try:
    from django.utils.module_loading import import_string
except ImportError:
    # django 1.4
    from importlib import import_module

    def import_string(path):
        i = path.rfind('.')
        return getattr(import_module(path[:i]), path[i + 1:])
