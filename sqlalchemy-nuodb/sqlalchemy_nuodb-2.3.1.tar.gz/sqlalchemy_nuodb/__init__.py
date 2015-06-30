__version__ = '2.3.1'

from sqlalchemy.dialects import registry

from . import base, pynuodb

base.dialect = pynuodb.dialect

from .base import \
    NUMBER, dialect

__all__ = (
    'NUMBER', 'dialect'
)

registry.register("nuodb", "sqlalchemy_nuodb.pynuodb", "NuoDBDialect_pynuodb")
registry.register("nuodb.pynuodb", "sqlalchemy_nuodb.pynuodb", "NuoDBDialect_pynuodb")
