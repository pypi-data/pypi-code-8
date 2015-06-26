import warnings

warnings.warn("bright_fabric.fabfile is deprecated. Use bright_fabric.tasks instead", DeprecationWarning)

from .tasks import *  # NOQA
