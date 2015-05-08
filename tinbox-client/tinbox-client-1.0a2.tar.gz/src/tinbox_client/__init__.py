from . import version
from .client import Tinbox

__all__ = ['Tinbox', '__version__']

__version__ = version.get_version()
