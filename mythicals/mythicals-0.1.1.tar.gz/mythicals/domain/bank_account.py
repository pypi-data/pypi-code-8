from __future__ import unicode_literals

import os

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
import sqlalchemy.ext.hybrid as sahybrid
import sqlalchemy.orm as saorm

from .. import Form, form
from .. import db
from . import Persisted, OpMixin, Submission, Settlement, Currencies


BankAccountCode = pg.ENUM(
    'UNKNOWN',
    name='bank_account_code',
    create_type=False,
)


BankAccountType = pg.ENUM(
    'SAVINGS',
    'CHECKING',
    name='bank_account_type',
    create_type=False
)


BankAccountOpType = pg.ENUM(
    'CREDIT',
    'DEBIT',
    'REVERSE_DEBIT',
    name='bank_account_op_type',
    create_type=False
)

BankAccountOpState = pg.ENUM(
    'STAGED',
    'EXECUTING',
    'SUCCEEDED',
    'FAILED',
    'CANCELED',
    name='bank_account_op_state',
    create_type=False,
)


bank_account_ops = sa.Table(
    'bank_account_ops',
    db.meta_data,
    sa.Column('id', db.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
    sa.Column('_type', BankAccountOpType, nullable=False),
    sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
    sa.Column('updated_at', sa.DateTime, nullable=False, onupdate=sa.func.clock_timestamp(), server_default=sa.text('now()')),
    sa.Column('company_id', db.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
    sa.Column('submission_id', db.UUID, sa.ForeignKey('submissions.id', ondelete='CASCADE'), nullable=False, index=True),
    sa.Column('confirmation_id', db.UUID, sa.ForeignKey('confirmations.id', ondelete='CASCADE'), nullable=False, index=True),
    sa.Column('settlement_id', db.UUID, sa.ForeignKey('settlements.id', ondelete='CASCADE'), index=True),
    sa.Column('external_id', sa.Unicode, nullable=False),
    sa.Column('trace_id', sa.Unicode, index=True, default=lambda: tracer.id, nullable=False,),
    sa.Column('reference_id', db.UUID, sa.ForeignKey('bank_account_ops.id'), index=True),
    sa.Column('account_number', sa.Unicode, nullable=False),
    sa.Column('account_type', BankAccountType, nullable=False),
    sa.Column('bank_code', sa.Unicode, nullable=False),
    sa.Column('country_code', sa.Unicode, nullable=False),
    sa.Column('params', db.JSON, nullable=False),
    sa.Column('state', BankAccountOpState, nullable=False, default='STAGED', server_default='STAGED'),
    sa.Column('code', BankAccountCode),
    sa.Column('diagnostics', pg.ARRAY(sa.Unicode), nullable=False, default=list, server_default=sa.text('array[]::varchar[]')),
)


class BankAccountOp(OpMixin, Persisted):

    __table__ = bank_account_ops

    __mapper_args__ = {
        'polymorphic_on': bank_account_ops.c._type,
    }

    types = db.Enum(BankAccountOpType)

    states = db.Enum(BankAccountOpState)

    codes = db.Enum(BankAccountCode)

    account_types = db.Enum(BankAccountType)

    reference = saorm.relationship('BankAccountOp', uselist=False)

    class NotStaged(Exception):

        pass


    class NotExecuting(Exception):

        pass

    class Submission(OpMixin.Submission):

        amount = form.Integer(min_value=0)

        code = form.String(choices=db.Enum(BankAccountCode), default=None)

        diagnostics = form.List(form.String(), default=None)

    class Params(OpMixin.Params):

        amount = form.Integer(min_value=0)

        currency = form.String(choices=Currencies)

        code = form.String(choices=db.Enum(BankAccountCode), default=None)

        diagnostics = form.List(form.String(), default=list)

    @classmethod
    def create(cls,
               confirmation,
               external_id,
               account_number,
               account_type,
               bank_code,
               country_code,
               trace_id=None,
               reference=None,
               **params
        ):
        params = cls.Params(params)
        op = cls(
            company=confirmation.company,
            submission=confirmation.submission,
            confirmation=confirmation,
            reference=reference,
            external_id=external_id,
            trace_id=trace_id,
            account_number=account_number,
            account_type=account_type,
            bank_code=bank_code,
            country_code=country_code,
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


class BankAccountCredit(BankAccountOp):

    __mapper_args__ = {
        'polymorphic_identity': BankAccountOp.types.CREDIT
    }

    @classmethod
    def tally(cls, ops):
        op_type = saorm.class_mapper(cls).polymorphic_identity
        ops_subq = ops.filter(cls._type == op_type).subquery()
        tally_q = (
            db.Session.query(
                cls._type.label('type'),
                cls.params[sa.literal('currency')].astext.label('currency'),
                sa.func.sum(cls.params[sa.literal('amount')].cast(sa.Integer)).label('amount'),
                sa.func.count(0).label('count')
            )
            .join(ops_subq, cls.id == ops_subq.c.id)
            .group_by('type', 'currency')
        )
        return map(dict, db.Session.execute(tally_q).fetchall())

    class Submission(BankAccountOp.Submission):

        currency = form.String(choices=Currencies)

        account_number = form.String()

        account_type = form.String(choices=BankAccountOp.account_types)

        bank_code = form.String()

        country_code = form.String()

    class Params(BankAccountOp.Params):

        poop = form.Integer(optional=True)

    def _execute(self):
        pass


db.as_form(BankAccountCredit.params, BankAccountCredit.Params, mutable=True)


class BankAccountDebit(BankAccountOp):

    __mapper_args__ = {
        'polymorphic_identity': BankAccountOp.types.DEBIT
    }

    @classmethod
    def tally(cls, ops):
        op_type = saorm.class_mapper(cls).polymorphic_identity
        ops_subq = ops.filter(cls._type == op_type).subquery()
        tally_q = (
            db.Session.query(
                cls._type.label('type'),
                cls.params[sa.literal('currency')].astext.label('currency'),
                sa.func.sum(cls.params[sa.literal('amount')].cast(sa.Integer)).label('amount'),
                sa.func.count(0).label('count')
            )
            .join(ops_subq, cls.id == ops_subq.c.id)
            .group_by('type', 'currency')
        )
        return map(dict, db.Session.execute(tally_q).fetchall())


    class Submission(BankAccountOp.Submission):

        currency = form.String(choices=Currencies)

        account_number = form.String()

        account_type = form.String(choices=BankAccountOp.account_types)

        bank_code = form.String()

        country_code = form.String()


    class Params(BankAccountOp.Params):

        pass

    def _execute(self):
        pass


db.as_form(BankAccountDebit.params, BankAccountDebit.Params)


class BankAccountReverseDebit(BankAccountOp):

    __mapper_args__ = {
        'polymorphic_identity': BankAccountOp.types.REVERSE_DEBIT
    }

    @classmethod
    def tally(cls, ops):
        op_type = saorm.class_mapper(cls).polymorphic_identity
        ops_subq = ops.filter(cls._type == op_type).subquery()
        debit_alias = saorm.aliased(BankAccountDebit)
        tally_q = (
            db.Session.query(
                cls._type.label('type'),
                debit_alias.params[sa.literal('currency')].astext.label('currency'),
                sa.func.sum(cls.params[sa.literal('amount')].cast(sa.Integer)).label('amount'),
                sa.func.count(0).label('count')
            )
            .join(ops_subq, cls.id == ops_subq.c.id)
            .join(debit_alias, cls.reference)
            .group_by('type', 'currency')
        )
        return map(dict, db.Session.execute(tally_q).fetchall())

    class Submission(BankAccountOp.Submission):

        debit = form.UUID('debit_id')

        @debit.munge
        def debit(self, value):
            debit = BankAccountDebit.query.get(value)
            if debit is None:
                self.ctx.errors.invalid(
                    '{} does not reference a bank account debit'.format(value)
                )
                return form.ERROR
            return debit


    class Params(BankAccountOp.Params):

        pass

    def _execute(self):
        pass


db.as_form(BankAccountReverseDebit.params, BankAccountReverseDebit.Params)


class BankAccountSubmission(Submission):

    __mapper_args__ = {
        'polymorphic_identity': Submission.types.BANK_ACCOUNT
    }

    ops = saorm.relationship('BankAccountOp', lazy='dynamic')

    credits = saorm.relationship('BankAccountCredit', lazy='dynamic')

    debits = saorm.relationship('BankAccountDebit', lazy='dynamic')

    reverse_debits = saorm.relationship('BankAccountReverseDebit', lazy='dynamic')

    def tally(self):
        tallies = []
        for type_ in BankAccountOp.types:
            op_cls = saorm.class_mapper(BankAccountOp).polymorphic_map[type_].class_
            tallies.extend(op_cls.tally(self.ops))
        return tallies

    class Form(Form):

        credit_count = form.Integer(min_value=0, default=0)

        credits = form.List(
            form.SubForm(BankAccountCredit.Submission), default=list
        )

        @credits.field.munge
        def credits(self, value):
            return BankAccountCredit.from_form(value)

        @credits.validate
        def credits(self, value):
            if len(value) != self.credit_count:
                self.ctx.errors.invalid(
                    'expected {} item(s), received {}'.format(self.credit_count, len(value))
                )
                return False
            return True

        debit_count = form.Integer(min_value=0, default=0)

        debits = form.List(
            form.SubForm(BankAccountDebit.Submission), default=list
        )

        @debits.validate
        def debits(self, value):
            if len(value) != self.debit_count:
                self.ctx.errors.invalid(
                    'expected {} item(s), received {}'.format(self.debit_count, len(value))
                )
                return False
            return True

        @debits.field.munge
        def debits(self, value):
            return BankAccountDebit.from_form(value)

        reverse_debit_count = form.Integer(min_value=0, default=0)

        reverse_debits = form.List(
            form.SubForm(BankAccountReverseDebit.Submission), default=list
        )

        @reverse_debits.validate
        def reverse_debits(self, value):
            if len(value) != self.reverse_debit_count:
                self.ctx.errors.invalid(
                    'expected {} item(s), received {}'.format(self.reverse_debit_count, len(value))
                )
                return False
            return True

        @reverse_debits.field.munge
        def reverse_debits(self, value):
            return BankAccountReverseDebit.from_form(form=value)

    @property
    def archive_location(self):
        mime = self.mimes.match(self.mime_type)
        return os.path.join(
            'downloads',
            'bank_account',
            'submissions',
            '{0}.{1}'.format(self.external_id, mime.extension)
        )


class BankAccountSettlement(Settlement):

    __mapper_args__ = {
        'polymorphic_identity': Submission.types.BANK_ACCOUNT
    }

    op_type = BankAccountOp

    ops = saorm.relationship(
        'BankAccountOp', lazy='dynamic', backref='settlement',
    )

    @property
    def publish_path(self):
        return os.sep + os.path.join(
            str(self.company.id), 'bank_account', 'settlements', str(self.id)
        )
