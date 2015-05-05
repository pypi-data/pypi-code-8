import logging

from omnomnom import models


def validate_executable(executable):

    if isinstance(executable, models.Executable):
        if not hasattr(executable, '__call__'):
            msg = u"{0} must have __call__ defined".format(
                executable.__class__.__name__
            )
            return False, msg
        else:
            return True, None

    msg = (
        u"Cannot register executable {0}. "
        u"It must be an instance of models.Executable."
    ).format(executable)
    return False, msg


def register_executable(class_, registry, name, *args, **kwargs):

    def wrapper(c):
        instance = c(*args, **kwargs)
        is_valid, error = validate_executable(executable=instance)

        if is_valid:
            registry[name] = instance
        else:
            logging.warning(error)

        return c

    return wrapper(class_)