__all__ = [
    'init',
    'exc',
    'Currency',
    'Currencies',
    'Company',
    'Confirmation',
    'Submission',
    'Settlement',
    'Merchant',
    'MerchantOp',
    'MerchantSubmission',
    'MerchantSettlement',
    'CreditCardAddress',
    'CreditCardVerification',
    'CreditCardHold',
    'CreditCardOp',
    'CreditCardCaptureHold',
    'CreditCardVoidHold',
    'CreditCardReverseHoldCapture',
    'CreditCardCredit',
    'CreditCardSubmission',
    'CreditCardSettlement',
    'BankAccountOp',
    'BankAccountCredit',
    'BankAccountDebit',
    'BankAccountReverseDebit',
    'BankAccountSubmission',
    'BankAccountSettlement',
]

import uuid

import sqlalchemy as sa
import sqlalchemy.exc as saexc
import sqlalchemy.ext.declarative as sadecl
import sqlalchemy.ext.hybrid as sahybrid
import sqlalchemy.orm as saorm
import sqlalchemy.dialects.postgresql as pg

from .. import db, form, Form


def init(config):
    pass


@sadecl.as_declarative()
class Persisted(db.Model):

    generate_id = staticmethod(uuid.uuid4)


InstrumentType = pg.ENUM(
    'BANK_ACCOUNT',
    'CREDIT_CARD',
    'MERCHANT',
    name='instrument_type',
    create_type=False
)

class OpMixin(object):

    @sadecl.declared_attr
    def company(cls):
        return saorm.relationship('Company')

    @sadecl.declared_attr
    def submission(cls):
        return saorm.relationship('Submission')

    @sadecl.declared_attr
    def confirmation(cls):
        return saorm.relationship('Confirmation')

    @sahybrid.hybrid_property
    def confirmed(self):
        return self.confirmation_id != None

    @sahybrid.hybrid_property
    def executed(self):
        return self.state in (
            self.states.SUCCEEDED, self.states.FAILED
        )

    @executed.expression
    def executed(cls):
        return cls.state.in_([
            cls.states.SUCCEEDED, cls.states.FAILED
        ])

    @sahybrid.hybrid_property
    def settled(self):
        return self.settlement_id != None

    class Submission(Form):

        confirmation = form.Field().from_context()

        trace_id = form.String(default=None).from_context()

        external_id = form.String()

    class Params(Form):

        pass

    @classmethod
    def tally(cls, ops):
        raise NotImplementedError()

    @classmethod
    def from_form(cls, form):
        return cls.create(**form)

    def __call__(self):
        self._executing()
        if self.params.code:
            self._failed(self.params.code, self.params.diagnostics)
        else:
            try:
                self._execute()
            except Exception as ex:
                self._failed(ex.code, [str(ex)])
            else:
                self._succeeded()
        return self


    def _executing(self):
        count = (
            type(self).query
            .filter(
                type(self).id == self.id,
                type(self).state == type(self).states.STAGED,
            )
            .update(
                values={
                    'state': type(self).states.EXECUTING
                }
            )
        )
        if count != 1:
            raise self.NotStaged(self)

    def _execute(self):
        raise NotImplementedError()

    def _succeeded(self):
        count = (
            type(self).query
            .filter(
                type(self).id == self.id,
                type(self).state == type(self).states.EXECUTING,
            )
            .update(
                values={
                    'state': type(self).states.SUCCEEDED
                }
            )
        )
        if count != 1:
            raise self.NotExecuting(self)

    def _failed(self, code, diagnostics):
        count = (
            type(self).query
            .filter(
                type(self).id == self.id,
                type(self).state == type(self).states.EXECUTING,
            )
            .update(
                values={
                    'state': type(self).states.FAILED,
                    'code': code,
                    'diagnostics': diagnostics,
                }
            )
        )
        if count != 1:
            raise self.NotExecuting(self)


from . import exc
from .currency import Currency, Currencies
from .company import Company
from .confirmation import Confirmation
from .submission import Submission
from .settlement import Settlement
from .merchant import (
    Merchant,
    MerchantOp,
    MerchantSubmission,
    MerchantSettlement,
)
from .credit_card import (
    CreditCardAddress,
    CreditCardVerification,
    CreditCardHold,
    CreditCardOp,
    CreditCardCaptureHold,
    CreditCardVoidHold,
    CreditCardReverseHoldCapture,
    CreditCardCredit,
    CreditCardSubmission,
    CreditCardSettlement,
)
from .bank_account import (
    BankAccountOp,
    BankAccountCredit,
    BankAccountDebit,
    BankAccountReverseDebit,
    BankAccountSubmission,
    BankAccountSettlement,
)
