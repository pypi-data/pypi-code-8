import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
import sqlalchemy.orm as saorm

from .. import mime, db
from . import Persisted, InstrumentType


ConfirmationCode = pg.ENUM(
    'STAGED',
    'ACCEPTED',
    'MALFORMED',
    name='confirmation_code',
    create_type=False,
)

confirmations = sa.Table(
    'confirmations',
    db.meta_data,
    sa.Column('id', db.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
    sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
    sa.Column('company_id', db.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
    sa.Column('code', ConfirmationCode, nullable=False),
    sa.Column('diagnostics', pg.ARRAY(sa.Unicode), server_default=sa.text('array[]::varchar[]')),
)


class Confirmation(Persisted):

    __table__ = confirmations

    types = db.Enum(InstrumentType)

    codes = db.Enum(ConfirmationCode)

    company = saorm.relationship('Company')

    mimes = mime.Selection([mime.json])

    @classmethod
    def create(cls, company, code, diagnostics=None, id=None):
        confirmation = cls(
            id=id or cls.generate_id(),
            company=company,
            code=code,
            diagnostics=diagnostics or []
        )
        db.Session.add(confirmation)
        return confirmation
