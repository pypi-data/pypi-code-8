from __future__ import unicode_literals

import os

import sqlalchemy as sa
import sqlalchemy.orm as saorm
import sqlalchemy.dialects.postgresql as pg
import sqlalchemy.ext.hybrid as sahybrid

from mythicals import db, form, tracer

from . import Persisted, OpMixin, Submission, Settlement


MerchantCode = pg.ENUM(
    'UNKNOWN',
    'EVIL',
    name='merchant_code',
    create_type=False,
)

MerchantOpType = pg.ENUM(
    'UNDERWRITE',
    name='merchant_op_type',
    create_type=False
)

MerchantOpState = pg.ENUM(
    'STAGED',
    'EXECUTING',
    'SUCCEEDED',
    'FAILED',
    'CANCELED',
    name='merchant_op_state',
    create_type=False
)

merchant_ops = sa.Table(
    'merchant_ops',
    db.meta_data,
    sa.Column('id', db.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
    sa.Column('_type', MerchantOpType, nullable=False),
    sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
    sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
    sa.Column('company_id', db.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
    sa.Column('submission_id', db.UUID, sa.ForeignKey('submissions.id', ondelete='CASCADE'), nullable=False, index=True),
    sa.Column('confirmation_id', db.UUID, sa.ForeignKey('confirmations.id', ondelete='CASCADE'), nullable=False, index=True),
    sa.Column('settlement_id', db.UUID, sa.ForeignKey('settlements.id', ondelete='CASCADE'), index=True),
    sa.Column('external_id', sa.Unicode, nullable=False),
    sa.Column('trace_id', sa.Unicode, index=True, default=lambda: tracer.id, nullable=False),
    sa.Column('params', pg.JSON, nullable=False),
    sa.Column('state', MerchantOpState, nullable=False, server_default='STAGED'),
    sa.Column('code', MerchantCode),
    sa.Column('diagnostics', pg.ARRAY(sa.Unicode), nullable=False, server_default=sa.text('array[]::varchar[]')),
)


merchants = sa.Table(
    'merchants',
    db.meta_data,
    sa.Column('id', db.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
    sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
    sa.Column('updated_at', sa.DateTime, nullable=False, onupdate=sa.func.clock_timestamp(), server_default=sa.text('now()')),
    sa.Column('company_id', db.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
    sa.Column('trace_id', sa.Unicode, index=True, default=lambda: tracer.id, nullable=False),
    sa.Column('name', sa.Unicode, nullable=False),
    sa.Column('phone_number', sa.Unicode, nullable=False),
    sa.Column('tax_id', sa.Unicode, nullable=False),
    sa.Column('country_code', sa.Unicode, nullable=False),
)



class MerchantOp(OpMixin, Persisted):

    __table__ = merchant_ops

    __mapper_args__ = {
        'polymorphic_on': merchant_ops.c._type,
    }

    types = db.Enum(MerchantOpType)

    states = db.Enum(MerchantOpState)

    codes = db.Enum(MerchantCode)

    class Submission(OpMixin.Submission):

        code = form.String(choices=db.Enum(MerchantCode), default=None)

        diagnostics = form.List(form.String(), default=None)

    class Params(OpMixin.Params):

        code = form.String(choices=db.Enum(MerchantCode), default=None)

        diagnostics = form.List(form.String(), default=list)

    @classmethod
    def create(cls,
               confirmation,
               external_id,
               trace_id=None,
               **params
        ):
        params = cls.Params(params)
        op = cls(
            company=confirmation.company,
            submission=confirmation.submission,
            confirmation=confirmation,
            external_id=external_id,
            trace_id=trace_id,
            params=params,
        )
        db.Session.add(op)
        return op

    @sahybrid.hybrid_property
    def has_settlement(self):
        return self.settlement_id != None

    @sahybrid.hybrid_property
    def has_confirmation(self):
        return self.confirmation_id != None


class MerchantUnderwrite(MerchantOp):

    __mapper_args__ = {
        'polymorphic_identity': MerchantOp.types.UNDERWRITE,
    }

    @classmethod
    def tally(cls, ops):
        op_type = saorm.class_mapper(cls).polymorphic_identity
        ops_subq = ops.filter(cls._type == op_type).subquery()
        tally_q = (
            db.Session.query(
                MerchantOp._type.label('type'),
                sa.func.count(0).label('count')
            )
            .join(ops_subq, MerchantOp.id == ops_subq.c.id)
            .group_by('type')
        )
        return map(dict, db.Session.execute(tally_q).fetchall())

    class Submission(MerchantOp.Submission):

        name = form.String()

        phone_number = form.String()

        tax_id = form.String()

        country_code = form.String()


    class Params(MerchantOp.Params):

        _type = form.String().constant('merchant.underwrite.params.v1')

        name = form.String()

        phone_number = form.String()

        tax_id = form.String()

        country_code = form.String()

    def _execute(self):
        Merchant.create(
            company=self.company,
            name=self.params.name,
            phone_number=self.params.phone_number,
            tax_id=self.params.tax_id,
            country_code=self.params.country_code,
        )


db.as_form(MerchantUnderwrite.params, MerchantUnderwrite.Params)


class Merchant(Persisted):

    __table__ = merchants

    company = saorm.relationship('Company')

    @classmethod
    def create(cls,
               company,
               name,
               phone_number,
               tax_id,
               country_code,
               id=None,
               trace_id=None
        ):
        merchant = Merchant(
            company=company,
            name=name,
            phone_number=phone_number,
            tax_id=tax_id,
            country_code=country_code,
        )
        db.Session.add(merchant)
        return merchant


class MerchantSubmission(Submission):

    __mapper_args__ = {
        'polymorphic_identity': Submission.types.MERCHANT
    }

    ops = saorm.relationship('MerchantOp', lazy='dynamic')

    underwrites = saorm.relationship('MerchantUnderwrite', lazy='dynamic')


    def tally(self):
        tallies = []
        for type_ in MerchantOp.types:
            op_cls = saorm.class_mapper(MerchantOp).polymorphic_map[type_].class_
            tallies.extend(op_cls.tally(self.ops))
        return tallies

    class Form(form.Form):

        underwrite_count = form.Integer(min_value=0, default=0)

        underwrites = form.List(
            form.SubForm(MerchantUnderwrite.Submission), default=list
        )

        @underwrites.field.munge
        def underwrites(self, value):
            return MerchantUnderwrite.from_form(value)

    @property
    def archive_location(self):
        mime = self.mimes.match(self.mime_type)
        return os.path.join(
            'downloads',
            'merchant',
            'submissions',
            '{0}.{1}'.format(self.external_id, mime.extension)
        )


class MerchantSettlement(Settlement):

    __mapper_args__ = {
        'polymorphic_identity': Settlement.types.MERCHANT
    }

    op_type = MerchantOp

    ops = saorm.relationship('MerchantOp', lazy='dynamic', backref='settlement')

    @property
    def publish_path(self):
        return os.sep + os.path.join(
            str(self.company.id),
            'merchant',
            'settlements',
            str(self.id)
        )
