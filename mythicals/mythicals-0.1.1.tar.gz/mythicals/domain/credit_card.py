from __future__ import unicode_literals

import os

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
import sqlalchemy.orm as saorm
import sqlalchemy.ext.hybrid as sahybrid

from mythicals import Form, form, db, tracer

from . import Persisted, OpMixin, Currency, Submission, Settlement, Currencies, exc



CreditCardCode = pg.ENUM(
    'UNKNOWN',
    'DECLINED',
    'LOCKED',
    name='credit_card_code',
    create_type=False,
)

class CreditCardAddress(Form):

    street = form.String(default=None)

    city = form.String(default=None)

    region = form.String(default=None)

    country_code = form.String(default=None)

    postal_code = form.String(default=None)


CreditCardVerificationState = pg.ENUM(
    'STAGED',
    'ACCEPTED',
    'REJECTED',
    name='credit_card_verification_state',
    create_type=False
)


credit_card_verifications = sa.Table(
    'credit_card_verifications',
    db.meta_data,
    sa.Column('id', db.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
    sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
    sa.Column('updated_at', sa.DateTime, nullable=False, onupdate=sa.func.clock_timestamp(), server_default=sa.text('now()')),
    sa.Column('company_id', db.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
    sa.Column('external_id', sa.Unicode, nullable=False),
    sa.Column('trace_id', sa.Unicode, index=True, default=lambda: tracer.id, nullable=False),
    sa.Column('card_number', sa.Unicode, nullable=False),
    sa.Column('card_security_code', sa.Unicode),
    sa.Column('address', db.JSON),
    sa.Column('phone_number', sa.Unicode),
    sa.Column('params', db.JSON, nullable=False),
    sa.Column('state', CreditCardVerificationState, default='STAGED', server_default='STAGED', nullable=False),
    sa.Column('address_matched', sa.Boolean),
    sa.Column('postal_code_matched', sa.Boolean),
    sa.Column('security_code_matched', sa.Boolean),
    sa.Column('code', CreditCardCode),
    sa.Column('diagnostics', pg.ARRAY(sa.Unicode), nullable=False, server_default=sa.text('array[]::varchar[]')),
)

class CreditCardVerification(Persisted):

    __table__ = credit_card_verifications

    company = saorm.relationship('Company')

    states = db.Enum(CreditCardVerificationState)

    codes = db.Enum(CreditCardCode)

    class Params(Form):

        code = form.String(choices=db.Enum(CreditCardCode), default=None)

        diagnostics = form.List(form.String(), default=list)

        address_matched = form.Boolean(default=None)

        postal_code_matched = form.Boolean(default=None)

        security_code_matched = form.Boolean(default=None)

    @classmethod
    def create(cls,
               company,
               external_id,
               card_number,
               card_security_code=None,
               address=None,
               phone_number=None,
               id=None,
               trace_id=None,
               params=None,
        ):
        if address:
            address = CreditCardAddress(address)
        params = cls.Params(params or {})
        hold = cls(
            id=id or cls.generate_id(),
            company=company,
            external_id=external_id,
            trace_id=trace_id,
            card_number=card_number,
            card_security_code=card_security_code,
            address=address,
            phone_number=phone_number,
            params=params,
        )
        db.Session.add(hold)
        return hold

    def inquire(self):
        if self.params.code is not None:
            state = self.states.REJECTED
            code = self.params.code
            diagnostics = self.params.diagnostics
            address_matched = None
            postal_code_matched = None
            security_code_matched = None
        else:
            state = self.states.ACCEPTED
            code = None
            diagnostics = []
            address_matched = self.params.address_matched
            if address_matched is None:
                address_matched = True
            postal_code_matched = self.params.postal_code_matched
            if postal_code_matched is None:
                postal_code_matched = True
            security_code_matched = self.params.security_code_matched
            if security_code_matched is None:
                security_code_matched = True
        count = self._transition([
                CreditCardVerification.state == self.states.STAGED,
            ],
            state=state,
            code=code,
            diagnostics=diagnostics,
            address_matched=address_matched,
            postal_code_matched=postal_code_matched,
            security_code_matched=security_code_matched,
        )
        if count != 1:
            raise exc.VerificationNotStaged(self)
        return self

    def _transition(self, filters, **values):
        return (
            CreditCardVerification
            .query
            .filter(
                CreditCardVerification.id == self.id,
                *filters
            )
            .update(
                values=values,
                synchronize_session='fetch',
            )
        )


db.as_form(CreditCardVerification.params, CreditCardVerification.Params)


CreditCardHoldState = pg.ENUM(
    'STAGED',
    'OPEN',
    'CAPTURED',
    'VOIDED',
    'REJECTED',
    name='credit_card_hold_state',
    create_type=False
)

credit_card_hold = sa.Table(
    'credit_card_holds',
    db.meta_data,
    sa.Column('id', db.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
    sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
    sa.Column('updated_at', sa.DateTime, nullable=False, onupdate=sa.func.clock_timestamp(), server_default=sa.text('now()')),
    sa.Column('company_id', db.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
    sa.Column('external_id', sa.Unicode, nullable=False),
    sa.Column('trace_id', sa.Unicode, index=True, default=lambda: tracer.id, nullable=False),
    sa.Column('card_number', sa.Unicode, nullable=False),
    sa.Column('card_security_code', sa.Unicode),
    sa.Column('amount', sa.Integer, nullable=False),
    sa.Column('currency', Currency, nullable=False),
    sa.Column('captured_amount', sa.Integer, nullable=False, default=0, server_default='0'),
    sa.Column('params', db.JSON, nullable=False),
    sa.Column('state', CreditCardHoldState, default='STAGED', server_default='STAGED', nullable=False),
    sa.Column('code', CreditCardCode),
    sa.Column('diagnostics', pg.ARRAY(sa.Unicode), nullable=False, server_default=sa.text('array[]::varchar[]')),
)


class CreditCardHold(Persisted):

    __table__ = credit_card_hold

    codes = db.Enum(CreditCardCode)

    states = db.Enum(CreditCardHoldState)

    company = saorm.relationship('Company')

    captures = saorm.relationship('CreditCardCaptureHold', lazy='dynamic')

    reverses = saorm.relationship('CreditCardReverseHoldCapture', lazy='dynamic')

    voids = saorm.relationship('CreditCardVoidHold', lazy='dynamic')

    class Params(Form):

        code = form.String(choices=db.Enum(CreditCardCode), default=None)

        diagnostics = form.List(form.String(), default=list)

    @classmethod
    def create(cls,
               company,
               external_id,
               card_number,
               card_security_code,
               amount,
               currency,
               id=None,
               trace_id=None,
               params=None,
        ):
        params = cls.Params(params or {})
        hold = cls(
            id=id or cls.generate_id(),
            company=company,
            external_id=external_id,
            trace_id=trace_id,
            card_number=card_number,
            card_security_code=card_security_code,
            amount=amount,
            currency=currency,
            params=params,
        )
        db.Session.add(hold)
        return hold

    def open(self):
        if self.params.code is not None:
            return self.reject(self.params.code, self.params.diagnostics)
        count = self._transition([
                CreditCardHold.state == CreditCardHold.states.STAGED,
            ],
            state=self.states.OPEN,
        )
        if count != 1:
            raise exc.HoldNotStaged(self)
        return self

    def reject(self, code, diagnostics=None):
        diagnostics = diagnostics or []
        count = self._transition([
                CreditCardHold.state == CreditCardHold.states.STAGED,
            ],
            state=CreditCardHold.states.REJECTED,
            code=code,
            diagnostics=diagnostics,
        )
        if count != 1:
            raise exc.HoldNotStaged(self)
        return self

    def capture(self, amount):
        count = self._transition([
                CreditCardHold.state == CreditCardHold.states.OPEN,
                CreditCardHold.amount - CreditCardHold.captured_amount >= amount,
            ],
            captured_amount=CreditCardHold.captured_amount + amount,
            state=sa.cast(
                sa.case([(
                        CreditCardHold.amount - CreditCardHold.captured_amount == amount,
                        CreditCardHold.states.CAPTURED
                    )],
                    else_=CreditCardHold.states.OPEN,
                ),
                CreditCardHoldState
            ),
        )
        if count != 1:
            if self.state != CreditCardHold.states.OPEN:
                raise exc.HoldNotOpen(self)
            raise exc.InvalidHoldCaptureAmount(self, amount)
        return self

    def void(self):
        count = self._transition([
                CreditCardHold.state.in_([CreditCardHold.states.OPEN]),
            ],
            state=CreditCardHold.states.VOIDED
        )
        if count != 1:
            raise exc.HoldNotOpen(self)
        return self

    def _transition(self, filters, **values):
        return (
            CreditCardHold
            .query
            .filter(
                CreditCardHold.id == self.id,
                *filters
            )
            .update(
                values=values,
                synchronize_session='fetch',
            )
        )

db.as_form(CreditCardHold.params, CreditCardHold.Params)

CreditCardOpType = pg.ENUM(
    'CAPTURE_HOLD',
    'REVERSE_HOLD_CAPTURE',
    'VOID_HOLD',
    'CREDIT',
    name='credit_card_op_type',
    create_type=False
)


CreditCardOpState = pg.ENUM(
    'STAGED',
    'EXECUTING',
    'SUCCEEDED',
    'FAILED',
    name='credit_card_op_state',
    create_type=False
)


credit_card_ops = sa.Table(
    'credit_card_ops',
    db.meta_data,
    sa.Column('id', db.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
    sa.Column('_type', CreditCardOpType, nullable=False),
    sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
    sa.Column('company_id', db.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
    sa.Column('submission_id', db.UUID, sa.ForeignKey('submissions.id', ondelete='CASCADE'), nullable=False, index=True),
    sa.Column('confirmation_id', db.UUID, sa.ForeignKey('confirmations.id', ondelete='CASCADE'), nullable=False, index=True),
    sa.Column('settlement_id', db.UUID, sa.ForeignKey('settlements.id', ondelete='CASCADE'), index=True),
    sa.Column('external_id', sa.Unicode, nullable=False),
    sa.Column('trace_id', sa.Unicode, index=True, default=lambda: tracer.id, nullable=False),
    sa.Column('hold_id', db.UUID, sa.ForeignKey('credit_card_holds.id', ondelete='CASCADE'), index=True),
    sa.Column('card_number', sa.Unicode, nullable=False),
    sa.Column('card_security_code', sa.Unicode),
    sa.Column('params', db.JSON, nullable=False),
    sa.Column('state', CreditCardOpState, nullable=False, default='STAGED', server_default='STAGED'),
    sa.Column('code', CreditCardCode),
    sa.Column('diagnostics', pg.ARRAY(sa.Unicode), nullable=False, default=list, server_default=sa.text('array[]::varchar[]')),
)


class CreditCardOp(OpMixin, Persisted):

    __table__ = credit_card_ops

    __mapper_args__ = {
        'polymorphic_on': credit_card_ops.c._type
    }

    types = db.Enum(CreditCardOpType)

    states = db.Enum(CreditCardOpState)

    codes = db.Enum(CreditCardCode)

    class NotStaged(Exception):

        pass

    class NotExecuting(Exception):

        pass

    hold = saorm.relationship('CreditCardHold')

    class Submission(OpMixin.Submission):

        code = form.String(choices=db.Enum(CreditCardCode), default=None)

        diagnostics = form.List(form.String(), default=None)

    class Params(Form):

        code = form.String(choices=db.Enum(CreditCardCode), default=None)

        diagnostics = form.List(form.String(), default=list)

    @classmethod
    def create(cls,
               confirmation,
               external_id,
               card_number=None,
               card_security_code=None,
               hold=None,
               trace_id=None,
               **params
        ):
        if not card_number and hold:
            card_number = hold.card_number
        if not card_security_code and hold:
            card_security_code = hold.card_security_code
        params = cls.Params(params)
        op = cls(
            company=confirmation.company,
            submission=confirmation.submission,
            confirmation=confirmation,
            external_id=external_id,
            trace_id=trace_id,
            card_number=card_number,
            card_security_code=card_security_code,
            hold=hold,
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


class CreditCardCaptureHold(CreditCardOp):

    __mapper_args__ = {
        'polymorphic_identity': CreditCardOp.types.CAPTURE_HOLD
    }

    @classmethod
    def tally(cls, ops):
        op_type = saorm.class_mapper(cls).polymorphic_identity
        ops_subq = ops.filter(cls._type == op_type).subquery()
        tally_q = (
            db.Session.query(
                CreditCardOp._type.label('type'),
                CreditCardHold.currency.label('currency'),
                sa.func.sum(
                    CreditCardOp.params[sa.literal('amount')].cast(sa.Integer),
                ).label('amount'),
                sa.func.count(0).label('count')
            )
            .join(ops_subq, CreditCardOp.id == ops_subq.c.id)
            .join(CreditCardHold, CreditCardHold.id == ops_subq.c.hold_id)
            .group_by('type', 'currency')
        )
        return map(dict, db.Session.execute(tally_q).fetchall())

    class Submission(CreditCardOp.Submission):

        amount = form.Integer(min_value=0)

        hold = form.String('hold_id')

        @hold.parse
        def hold(self, path):
            return self.ctx.id_codecs.decode(path.primitive(basestring))

        @hold.munge
        def hold(self, value):
            hold = CreditCardHold.query.get(value)
            if hold is None:
                self.ctx.errors.invalid(
                    '{} does not reference a credit card hold'.format(value)
                )
                return form.ERROR
            return hold


    class Params(CreditCardOp.Params):

        _type = form.String().constant('credit_card.capture_hold.params.v1')

        amount = form.Integer(min_value=0)

    def _execute(self):
        self.hold.capture(self.params.amount)


db.as_form(CreditCardCaptureHold.params, CreditCardCaptureHold.Params)


class CreditCardVoidHold(CreditCardOp):

    __mapper_args__ = {
        'polymorphic_identity': CreditCardOp.types.VOID_HOLD
    }

    @classmethod
    def tally(cls, ops):
        op_type = saorm.class_mapper(cls).polymorphic_identity
        ops_subq = ops.filter(cls._type == op_type).subquery()
        tally_q = (
            db.Session.query(
                CreditCardOp._type.label('type'),
                sa.func.count(0).label('count')
            )
            .join(
                ops_subq, CreditCardOp.id == ops_subq.c.id
            )
            .group_by(
                'type'
            )
        )
        return map(dict, db.Session.execute(tally_q).fetchall())

    class Submission(CreditCardOp.Submission):

        hold = form.String('hold_id')

        @hold.parse
        def hold(self, path):
            return self.ctx.id_codecs.decode(path.primitive(basestring))

        @hold.munge
        def hold(self, value):
            hold = CreditCardHold.query.get(value)
            if hold is None:
                self.ctx.errors.invalid(
                    '{} does not reference a credit card hold'.format(value)
                )
                return form.ERROR
            return hold


    class Params(CreditCardOp.Params):

        _type = form.String().constant('credit_card.void_hold.params.v1')

    def _execute(self):
        self.hold.void()


db.as_form(CreditCardVoidHold.params, CreditCardVoidHold.Params)


class CreditCardReverseHoldCapture(CreditCardOp):

    __mapper_args__ = {
        'polymorphic_identity': CreditCardOp.types.REVERSE_HOLD_CAPTURE
    }

    @classmethod
    def tally(cls, ops):
        op_type = saorm.class_mapper(cls).polymorphic_identity
        ops_subq = ops.filter(cls._type == op_type).subquery()
        tally_q = (
            db.Session.query(
                CreditCardOp._type.label('type'),
                CreditCardHold.currency.label('currency'),
                sa.func.sum(
                    CreditCardOp.params[sa.literal('amount')].cast(sa.Integer),
                ).label('amount'),
                sa.func.count(0).label('count')
            )
            .join(ops_subq, CreditCardOp.id == ops_subq.c.id)
            .join(CreditCardHold, CreditCardHold.id == ops_subq.c.hold_id)
            .group_by('type', 'currency',)
        )
        return map(dict, db.Session.execute(tally_q).fetchall())

    class Submission(CreditCardOp.Submission):

        amount = form.Integer(min_value=0)

        hold = form.String('hold_id')

        @hold.parse
        def hold(self, path):
            return self.ctx.id_codecs.decode(path.primitive(basestring))

        @hold.munge
        def hold(self, value):
            hold = CreditCardHold.query.get(value)
            if hold is None:
                self.ctx.errors.invalid(
                    '{} does not reference a credit card hold'.format(value)
                )
                return form.ERROR
            return hold


    class Params(CreditCardOp.Params):

        _type = form.String().constant('credit_card.reverse_hold_capture.params.v1')

        amount = form.Integer(min_value=0)

    def _execute(self):
        pass


db.as_form(CreditCardReverseHoldCapture.params, CreditCardReverseHoldCapture.Params)


class CreditCardCredit(CreditCardOp):

    __mapper_args__ = {
        'polymorphic_identity': CreditCardOp.types.CREDIT
    }

    @classmethod
    def tally(cls, ops):
        op_type = saorm.class_mapper(cls).polymorphic_identity
        ops_subq = ops.filter(cls._type == op_type).subquery()
        tally_q = (
            db.Session.query(
                CreditCardOp._type.label('type'),
                CreditCardOp.params[sa.literal('currency')].astext.label('currency'),
                sa.func.sum(
                    CreditCardOp.params[sa.literal('amount')].cast(sa.Integer),
                ).label('amount'),
                sa.func.count(0).label('count')
            )
            .join(
                ops_subq, CreditCardOp.id == ops_subq.c.id
            )
            .group_by('type', 'currency',)
        )
        return map(dict, db.Session.execute(tally_q).fetchall())

    class Submission(CreditCardOp.Submission):

        amount = form.Integer(min_value=0)

        currency = form.String(choices=Currencies)

        card_number = form.String()

        card_security_code = form.String(default=None)


    class Params(CreditCardOp.Params):

        _type = form.String().constant('credit_card.credit.params.v1')

        amount = form.Integer(min_value=0)

        currency = form.String(choices=Currencies)

    def _execute(self):
        pass


db.as_form(CreditCardCredit.params, CreditCardCredit.Params)


class CreditCardSubmission(Submission):

    __mapper_args__ = {
        'polymorphic_identity': Submission.types.CREDIT_CARD
    }

    ops = saorm.relationship('CreditCardOp', lazy='dynamic')

    capture_holds = saorm.relationship('CreditCardCaptureHold', lazy='dynamic')

    void_holds = saorm.relationship('CreditCardVoidHold', lazy='dynamic')

    reverse_hold_captures = saorm.relationship('CreditCardReverseHoldCapture', lazy='dynamic')

    credits = saorm.relationship('CreditCardCredit', lazy='dynamic')

    def tally(self):
        tallies = []
        for type_ in CreditCardOp.types:
            op_cls = saorm.class_mapper(CreditCardOp).polymorphic_map[type_].class_
            tallies.extend(op_cls.tally(self.ops))
        return tallies

    class Form(Form):

        capture_hold_count = form.Integer(min_value=0, default=0)

        capture_holds = form.List(
            form.SubForm(CreditCardCaptureHold.Submission), default=list
        )

        @capture_holds.field.munge
        def capture_holds_field(self, value):
            return CreditCardCaptureHold.from_form(value)

        reverse_hold_capture_count = form.Integer(min_value=0, default=0)

        reverse_hold_captures = form.List(
            form.SubForm(CreditCardReverseHoldCapture.Submission), default=list,
        )

        @reverse_hold_captures.field.munge
        def reverse_hold_captures_field(self, value):
            return CreditCardReverseHoldCapture.from_form(value)

        void_holds_count = form.Integer(min_value=0, default=0)

        void_holds = form.List(
            form.SubForm(CreditCardVoidHold.Submission), default=list,
        )

        @void_holds.field.munge
        def void_holds_field(self, value):
            return CreditCardVoidHold.from_form(value)

        credit_count = form.Integer(min_value=0, default=0)

        credits = form.List(
            form.SubForm(CreditCardCredit.Submission), default=list,
        )

        @credits.field.munge
        def credits(self, value):
            value.currency
            return CreditCardCredit.from_form(value)

    @property
    def archive_location(self):
        mime = self.mimes.match(self.mime_type)
        return os.path.join(
            'downloads',
            'credit_card',
            'submissions',
            '{0}.{1}'.format(self.external_id, mime.extension)
        )


class CreditCardSettlement(Settlement):

    __mapper_args__ = {
        'polymorphic_identity': Settlement.types.CREDIT_CARD
    }

    op_type = CreditCardOp

    ops = saorm.relationship('CreditCardOp', lazy='dynamic', backref='settlement')

    @property
    def publish_path(self):
        return os.sep + os.path.join(
            str(self.company.id), 'credit_card', 'settlements', str(self.id)
        )
