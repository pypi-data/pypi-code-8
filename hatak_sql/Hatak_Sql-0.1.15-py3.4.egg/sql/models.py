from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import AbstractConcreteBase

from hatak.unpackrequest import unpack

DeclatativeBase = declarative_base()


class Base(AbstractConcreteBase, DeclatativeBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = None

    def assign_request(self, request):
        self.request = request
        unpack(self, request)

    def __repr__(self):
        id_ = str(self.id) if self.id else 'None'
        return '%s (%s)' % (self.__class__.__name__, id_)
