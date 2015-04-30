__version__ = '0.1.0'


def handle_exception(err, app_obj):
    """Exception handler for processes running under manage.py."""

    from werkzeug.debug.tbtools import get_current_traceback
    traceback = get_current_traceback(ignore_system_exceptions=True)
    if hasattr(app_obj, 'script_logger'):
        app_obj.script_logger.error('%s\n\n%s' % (err, traceback.plaintext))
    else:
        raise err

