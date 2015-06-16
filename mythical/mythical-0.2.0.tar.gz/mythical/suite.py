import ConfigParser
import httplib
import logging
import os
import unittest
import uuid

import pytest

import mythical
from mythical import pilo


class Config(pilo.Form):

    username = pilo.fields.String(default='company')

    password = pilo.fields.String(default='password')

    http_root = pilo.fields.String(default='http://127.0.0.1:8080')

    http_headers = pilo.fields.Dict(
        pilo.fields.String(), pilo.fields.String(), default=dict
    )

    http_proxies = pilo.fields.Dict(
        pilo.fields.String(), pilo.fields.String(), default=None
    )

    sftp_host = pilo.fields.String(default='127.0.0.1')

    sftp_port = pilo.fields.Integer(default=8022)

    tokenize = pilo.fields.Code(default=None)

    @tokenize.munge
    def tokenize(self, value):
        if not hasattr(value, 'tokenize'):
            self.ctx.errors.invalid('missing tokenize callable')
            return pilo.NONE
        if callable(value):
            self.ctx.errors.invalid('tokenize is not callable')
            return pilo.NONE
        return value.tokenize


class ConfigOverrides(pilo.Form):

    username = pilo.fields.String('MYTHICAL_SUITE_USERNAME', optional=True).ignore(None)

    password = pilo.fields.String('MYTHICAL_SUITE_PASSWORD', optional=True).ignore(None)

    http_root = pilo.fields.String('MYTHICAL_SUITE_HTTP_ROOT', optional=True).ignore(None)

    sftp_host = pilo.fields.String('MYTHICAL_SUITE_SFTP_HOST', optional=True).ignore(None)

    sftp_port = pilo.fields.Integer('MYTHICAL_SUITE_SFTP_PORT', optional=True).ignore(None)


@pytest.fixture(scope='session')
def logging_level():
    return {
        'd': logging.DEBUG, 'debug': logging.DEBUG,
        'i': logging.INFO, 'info': logging.INFO,
        'w': logging.WARN, 'warn': logging.WARN,
    }[os.environ.get('MYTHICAL_SUITE_LOG', 'info').lower()]


@pytest.fixture(scope='session', autouse=True)
def logging_config(logging_level):
    if logging.NOTSET < logging_level <= logging.DEBUG:
        httplib.HTTPConnection.debuglevel = 1
    logging.basicConfig(level=logging_level)


class TestCase(unittest.TestCase):

    @classmethod
    def generate_trace_id(cls):
        return 'OHM-{}'.format(uuid.uuid4())

    @classmethod
    def tokenize_credit_card_number(cls, **fixture):
        if cls.tokenize and 'card_number' in fixture:
            fixture['card_number'] = cls.tokenize(fixture['card_number'])
        if cls.tokenize and 'card_security_code' in fixture:
            fixture['card_security_code'] = cls.tokenize(fixture['card_security_code'])
        return fixture

    @classmethod
    def tokenize_bank_account_number(cls, **fixture):
        if cls.tokenize and 'account_number' in fixture:
            fixture['account_number'] = cls.tokenize(fixture['account_number'])
        return fixture

    @classmethod
    def setUpClass(cls):
        super(TestCase, cls).setUpClass()

        config = Config({})

        config_path = os.path.expanduser(os.path.join('~', '.mythical'))
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_path)
        section = 'suite'
        if os.environ.get('MYTHICAL_SUITE'):
            section = '{}:{}'.format(section, os.environ.get('MYTHICAL_SUITE'))
        if config_parser.has_section(section):
            config_src = pilo.source.ConfigSource(
                config_parser,
                section=section,
                location=config_path,
                preserve_whitespace=True,
            )
            config.map(config_src, error='raise')
        else:
            config.update(ConfigOverrides(os.environ))

        mythical.configure(
            username=config.username,
            password=config.password,
            http_root=config.http_root,
            http_headers=config.http_headers,
            http_proxies=config.http_proxies,
            sftp_address=(config.sftp_host, config.sftp_port),
        )

        cls.tokenize = config.tokenize

    @classmethod
    def tearDownClass(cls):
        super(TestCase, cls).tearDownClass()

    def setUp(self):
        super(TestCase, self).setUp()
        self.trace_id = self.generate_trace_id()
        mythical.configure(trace_id=self.trace_id)

    def tearDown(self):
        mythical.configure(trace_id=None)
        super(TestCase, self).tearDown()


class TestCreditCard(TestCase):

    @classmethod
    def generate_external_id(cls):
        return 'MY-CC-{}'.format(uuid.uuid4())

    @classmethod
    def hold_fixture(cls, **overrides):
        fixture = {
            'external_id': cls.generate_external_id(),
            'card_number': '4' + '1' * 15,
            'card_security_code': '123',
            'amount': 12321,
            'currency': 'USD',
        }
        fixture.update(overrides)
        fixture = cls.tokenize_credit_card_number(**fixture)
        return fixture

    @classmethod
    def verification_fixture(cls, **overrides):
        fixture = {
            'external_id': cls.generate_external_id(),
            'card_number': '4' + '1' * 15,
            'card_security_code': '123',
            'address': {
                'street': '123 Crapware Lane',
                'city': 'Shitstack',
                'region': 'CA',
                'country_code': 'US',
                'postal_code': '90210',
            }
        }
        fixture.update(overrides)
        fixture = cls.tokenize_credit_card_number(**fixture)
        return fixture

    @classmethod
    def credit_fixture(cls, **overrides):
        fixture = {
            'external_id': cls.generate_external_id(),
            'card_number': '38123123123123',
            'card_security_code': '5531',
            'amount': 12312,
            'currency': 'CAD'
        }
        fixture.update(overrides)
        fixture = cls.tokenize_credit_card_number(**fixture)
        return mythical.credit_card.CreditSubmission(fixture)

    @classmethod
    def submission(cls):
        hold_1 = mythical.credit_card.Hold.open(**cls.hold_fixture())
        submit = mythical.credit_card.Submit(
            external_id=cls.generate_external_id(),
        )
        submit.capture_hold(
            external_id=cls.generate_external_id(),
            hold_id=hold_1.id,
            amount=hold_1.amount,
        )
        submit.reverse_hold_capture(
            external_id=cls.generate_external_id(),
            hold_id=hold_1.id,
            amount=hold_1.amount - 100,
        )
        submit.credits.append(cls.credit_fixture())
        return mythical.credit_card.Submit(submit)

    def test_ops(self):
        q = mythical.credit_card.Op.query().filter_by(trace_id=self.trace_id)
        self.assertEqual(q.count(), 0)
        submission = self.submission()()
        self.assertEqual(q.count(), 0)
        confirmation = submission.process()
        self.assertEqual(confirmation.code, 'ACCEPTED')
        self.assertEqual(q.count(), 3)

    def test_verification(self):
        verification = mythical.credit_card.Verification.inquire(
            **self.verification_fixture()
        )
        self.assertEqual(verification.state, 'ACCEPTED')
        self.assertTrue(verification.address_matched)
        self.assertTrue(verification.postal_code_matched)
        self.assertTrue(verification.security_code_matched)

        verification = mythical.credit_card.Verification.inquire(
            params={
                'address_matched': False,
                'postal_code_matched': True,
                'security_code_matched': True,
            },
            **self.verification_fixture()
        )
        self.assertEqual(verification.state, 'ACCEPTED')
        self.assertFalse(verification.address_matched)
        self.assertTrue(verification.postal_code_matched)
        self.assertTrue(verification.security_code_matched)


        verification = mythical.credit_card.Verification.inquire(
            params={
                'code': mythical.credit_card.Codes.UNKNOWN,
            },
            **self.verification_fixture()
        )
        self.assertEqual(verification.state, 'REJECTED')
        self.assertIsNone(verification.address_matched)
        self.assertIsNone(verification.postal_code_matched)
        self.assertIsNone(verification.security_code_matched)

    def test_hold(self):
        hold = mythical.credit_card.Hold.open(**self.hold_fixture())
        self.assertEqual(hold.state, 'OPEN')
        submit = mythical.credit_card.Submit(
            external_id=self.generate_external_id(),
        )
        submit.capture_hold(
            external_id=self.generate_external_id(),
            hold_id=hold.id,
            amount=hold.amount,
        )
        submission = submit()
        submission.process()
        hold.refresh()
        self.assertEqual(hold.state, 'OPEN')
        op = (
            mythical.credit_card.Op
            .query()
            .filter_by(trace_id=self.trace_id)
        ).first()
        op.execute()
        hold.refresh()
        self.assertEqual(hold.state, 'CAPTURED')

    def test_submit(self):
        hold_1 = mythical.credit_card.Hold.open(**self.hold_fixture())
        hold_2 = mythical.credit_card.Hold.open(**self.hold_fixture())
        submit = mythical.credit_card.Submit(
            external_id=self.generate_external_id(),
        )
        submit.capture_hold(
            external_id=self.generate_external_id(),
            hold_id=hold_1.id,
            amount=hold_1.amount,
        )
        submit.reverse_hold_capture(
            external_id=self.generate_external_id(),
            hold_id=hold_1.id,
            amount=hold_1.amount - 100,
        )
        submit.void_hold(
            external_id=self.generate_external_id(),
            hold_id=hold_2.id,
        )
        submit.credit(**self.credit_fixture())
        submission = submit()
        self.assertFalse(submission.processed)
        submission.process()
        submission.refresh()
        self.assertTrue(submission.processed)

    def test_cancel_submission(self):
        submission = self.submission()()
        submission.cancel()

    def test_force_fail(self):
        submit = mythical.credit_card.Submit(
            external_id=self.generate_external_id(),
        )
        submit.credit(**self.credit_fixture(
            code='DECLINED', diagnostics=['oops'],
        ))
        submission = submit()
        submission.process()
        submission.refresh()
        credit = submission.ops.first()
        self.assertEqual(credit.state, 'STAGED')
        self.assertEqual(credit.code, None)
        self.assertEqual(credit.diagnostics, [])
        credit()
        self.assertEqual(credit.state, 'FAILED')
        self.assertEqual(credit.code, 'DECLINED')
        self.assertEqual(credit.diagnostics, ['oops'])

    def test_settle(self):
        submission = self.submission()()
        submission.process()
        for op in submission.ops:
            self.assertEqual(op.state, 'STAGED')
            op.execute()
            self.assertNotEqual(op.state, 'STAGED')
            self.assertFalse(op.settled)
        settle = mythical.credit_card.Settle(
            trace_id=self.trace_id,
        )
        settlement = settle()
        self.assertItemsEqual(
            [op.id for op in submission.ops],
            [op.id for op in settlement.ops]
        )
        for op in submission.ops:
            self.assertTrue(op.settled)

    def test_sftp_submit(self):
        submit = self.submission()
        submit.upload()
        submission = (
            mythical.credit_card.Submission.query(external_id=submit.external_id)
        ).one()
        submission = submission.process()
        dowloaded = mythical.credit_card.Submit.download(submit.external_id)
        self.assertEqual(self.sanitize(submit), self.sanitize(dowloaded))

    def sanitize(self, submission):
        for credit in submission.credits:
            credit.pop('card_number')
            credit.pop('card_security_code')
        return submission


class TestBankAccount(TestCase):

    @classmethod
    def generate_external_id(cls):
        return 'MY-BA-{}'.format(uuid.uuid4())

    @classmethod
    def credit_fixture(cls, **overrides):
        fixture = {
            'external_id': cls.generate_external_id(),
            'account_number': 'fgf234wsfsdf',
            'account_type': 'SAVINGS',
            'bank_code': '35345',
            'country_code': 'CA',
            'amount': 4565,
            'currency': 'CAD',
        }
        fixture.update(overrides)
        fixture = cls.tokenize_bank_account_number(**fixture)
        return mythical.bank_account.CreditSubmission(fixture)

    @classmethod
    def debit_fixture(cls, **overrides):
        fixture = {
            'external_id': cls.generate_external_id(),
            'account_number': '234234234aa',
            'account_type': 'CHECKING',
            'bank_code': '35345',
            'country_code': 'US',
            'amount': 12321,
            'currency': 'USD',
        }
        fixture.update(overrides)
        fixture = cls.tokenize_bank_account_number(**fixture)
        return mythical.bank_account.DebitSubmission(fixture)

    @classmethod
    def submission(cls):
        return mythical.bank_account.Submit(
            external_id=cls.generate_external_id(),
            debits=[cls.debit_fixture()],
            credits=[cls.credit_fixture()],
        )

    def test_ops(self):
        q = mythical.bank_account.Op.query().filter_by(trace_id=self.trace_id)
        self.assertEqual(q.count(), 0)
        submission = self.submission()()
        self.assertEqual(q.count(), 0)
        confirmation = submission.process()
        self.assertEqual(confirmation.code, 'ACCEPTED')
        self.assertEqual(q.count(), 2)

    def test_cancel_submission(self):
        submission = self.submission()()
        submission.cancel()

    def test_submit(self):
        submission = self.submission()()
        self.assertFalse(submission.processed)
        submission.process()
        submission.refresh()
        self.assertTrue(submission.processed)

    def test_settle(self):
        submission = self.submission()()
        submission.process()
        for op in submission.ops:
            self.assertEqual(op.state, 'STAGED')
            op.execute()
            self.assertNotEqual(op.state, 'STAGED')
            self.assertFalse(op.settled)
        settle = mythical.bank_account.Settle(
            trace_id=self.trace_id,
        )
        settlement = settle()
        self.assertItemsEqual(
            [op.id for op in submission.ops],
            [op.id for op in settlement.ops]
        )
        for op in submission.ops:
            self.assertTrue(op.settled)

    def test_sftp_submit(self):
        submit = self.submission()
        submit.upload()
        submission = (
            mythical.bank_account.Submission.query(external_id=submit.external_id)
        ).one()
        submission = submission.process()
        dowloaded = mythical.bank_account.Submit.download(submit.external_id)
        self.assertEqual(self.sanitize(submit), self.sanitize(dowloaded))

    def sanitize(self, submission):
        for credit in submission.credits:
            credit.pop('account_number')
        for debits in submission.debits:
            debits.pop('account_number')
        for reverse_debit in submission.reverse_debits:
            reverse_debit.pop('account_number')
        return submission


class TestMerchant(TestCase):

    @classmethod
    def generate_external_id(cls):
        return 'MY-MC-{}'.format(uuid.uuid4())

    @classmethod
    def underwrite_fixture(cls, **overrides):
        fixture = {
            'external_id': cls.generate_external_id(),
            'name': 'me',
            'phone_number': '1-818-555-1212',
            'tax_id': '234124234234',
            'country_code': 'CA',
        }
        fixture.update(overrides)
        return mythical.merchant.UnderwriteSubmission(fixture)

    @classmethod
    def submission(cls):
        submit = mythical.merchant.Submit(
            external_id=cls.generate_external_id()
        )
        submit.underwrites.append(cls.underwrite_fixture())
        return submit()

    def test_ops(self):
        q = mythical.merchant.Op.query().filter_by(trace_id=self.trace_id)
        self.assertEqual(q.count(), 0)
        submission = self.submission()
        self.assertEqual(q.count(), 0)
        confirmation = submission.process()
        self.assertEqual(confirmation.code, 'ACCEPTED')
        self.assertEqual(q.count(), 1)


if __name__ == '__main__':
    import sys
    import pytest

    pytest.main(sys.argv)
