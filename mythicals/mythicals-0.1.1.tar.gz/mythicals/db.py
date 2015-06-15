__all__ = [
    'init',
    'engine',
    'meta_data',
    'Session',
    'UUID',
    'JSON',
    'Model',
    'Enum',
    'as_form',
]

import logging
import uuid

from sqlalchemy import create_engine, MetaData, TypeDecorator
from sqlalchemy.exc import InterfaceError
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import DetachedInstanceError
from sqlalchemy_pilo import as_form

from mythicals import Form, mime


logger = logging.getLogger(__name__)


def init(config):
    global engine

    engine = create_engine(
        config.DB['url'],
        json_serializer=mime.json.encode,
        **config.DB['kwargs']
    )
    Session.configure(bind=engine)


engine = None

meta_data = MetaData()

Session = scoped_session(sessionmaker())


def teardown_session():
    try:
        Session.rollback()
        Session.expunge_all()
        Session.remove()
    except InterfaceError, ex:
        if not ex.connection_invalidated:
            logger.exception(ex)
            raise
        Session.close()


class UUID(TypeDecorator):

    impl = postgresql.UUID

    def process_bind_param(self, value, dialect=None):
        if isinstance(value, uuid.UUID):
            return str(value)
        return value

    def process_result_value(self, value, dialect=None):
        if value is not None:
            return uuid.UUID(value)
        return None


class JSON(TypeDecorator):

    impl = postgresql.JSON

    def process_bind_param(self, value, dialect=None):
        if isinstance(value, Form):
            value = type(value)(value)
        return value


class Model(object):

    query = Session.query_property()

    def __str__(self):
        cols = self.__mapper__.c.keys()
        try:
            items = u', '.join([
                u'%s=%s' % (col, repr(getattr(self, col))) for col in cols
            ])
        except DetachedInstanceError:
            items = u'<detached>'
        return u'%s(%s)' % (self.__class__.__name__, items)


class Enum(list):

    def __init__(self, db_type):
        super(Enum, self).__init__(db_type.enums)
        for value in self:
            alias = value.upper()
            setattr(self, alias, value)


as_form = as_form
