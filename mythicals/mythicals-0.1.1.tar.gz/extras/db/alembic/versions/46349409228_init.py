"""init

Revision ID: 46349409228
Revises: None
Create Date: 2014-04-25 12:48:59.756770

"""

# revision identifiers, used by Alembic.
revision = '46349409228'
down_revision = None

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg


def upgrade():
    # common

    op.create_table(
        'companies',
        sa.Column('id', pg.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('name', sa.Unicode, unique=True, nullable=False, index=True),
    )

    op.create_table(
        'passwords',
        sa.Column('id', pg.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('company_id', pg.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('hashed', sa.Unicode, nullable=False),
    )

    # instruments

    InstrumentType = pg.ENUM(
        'CREDIT_CARD',
        'BANK_ACCOUNT',
        'MERCHANT',
        name='instrument_type',
        create_type=False
    )
    InstrumentType.create(bind=op.get_bind(), checkfirst=False)

    ConfirmationCode = pg.ENUM(
        'STAGED',
        'ACCEPTED',
        'MALFORMED',
        name='confirmation_code',
        create_type=False,
    )
    ConfirmationCode.create(bind=op.get_bind(), checkfirst=False)

    op.create_table(
        'confirmations',
        sa.Column('id', pg.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('company_id', pg.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('code', ConfirmationCode),
        sa.Column('diagnostics', pg.ARRAY(sa.Unicode), nullable=False, server_default=sa.text('array[]::varchar[]')),
    )

    op.create_table(
        'submissions',
        sa.Column('id', pg.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('_type', InstrumentType, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('company_id', pg.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('location', sa.Unicode, nullable=False),
        sa.Column('mime_type', sa.Unicode, nullable=False),
        sa.Column('external_id', sa.Unicode, nullable=False),
        sa.Column('trace_id', sa.Unicode, index=True),
        sa.Column('confirmation_id', pg.UUID, sa.ForeignKey('confirmations.id'), index=True),
    )

    op.create_table(
        'settlements',
        sa.Column('id', pg.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('_type', InstrumentType, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('company_id', pg.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('trace_id', sa.Unicode, index=True),
    )

    Currency = pg.ENUM(
        'AED',
        'AFN',
        'ALL',
        'AMD',
        'ANG',
        'AOA',
        'ARS',
        'AUD',
        'AWG',
        'AZN',
        'BAM',
        'BBD',
        'BDT',
        'BGN',
        'BHD',
        'BIF',
        'BMD',
        'BND',
        'BOB',
        'BOV',
        'BRL',
        'BSD',
        'BTN',
        'BWP',
        'BYR',
        'BZD',
        'CAD',
        'CDF',
        'CHE',
        'CHF',
        'CHW',
        'CLF',
        'CLP',
        'CNY',
        'COP',
        'COU',
        'CRC',
        'CUC',
        'CUP',
        'CVE',
        'CZK',
        'DJF',
        'DKK',
        'DOP',
        'DZD',
        'EGP',
        'ERN',
        'ETB',
        'EUR',
        'FJD',
        'FKP',
        'GBP',
        'GEL',
        'GHS',
        'GIP',
        'GMD',
        'GNF',
        'GTQ',
        'GYD',
        'HKD',
        'HNL',
        'HRK',
        'HTG',
        'HUF',
        'IDR',
        'ILS',
        'INR',
        'IQD',
        'IRR',
        'ISK',
        'JMD',
        'JOD',
        'JPY',
        'KES',
        'KGS',
        'KHR',
        'KMF',
        'KPW',
        'KRW',
        'KWD',
        'KYD',
        'KZT',
        'LAK',
        'LBP',
        'LKR',
        'LRD',
        'LSL',
        'LTL',
        'LYD',
        'MAD',
        'MDL',
        'MGA',
        'MKD',
        'MMK',
        'MNT',
        'MOP',
        'MRO',
        'MUR',
        'MVR',
        'MWK',
        'MXN',
        'MXV',
        'MYR',
        'MZN',
        'NAD',
        'NGN',
        'NIO',
        'NOK',
        'NPR',
        'NZD',
        'OMR',
        'PAB',
        'PEN',
        'PGK',
        'PHP',
        'PKR',
        'PLN',
        'PYG',
        'QAR',
        'RON',
        'RSD',
        'RUB',
        'RWF',
        'SAR',
        'SBD',
        'SCR',
        'SDG',
        'SEK',
        'SGD',
        'SHP',
        'SLL',
        'SOS',
        'SRD',
        'SSP',
        'STD',
        'SVC',
        'SYP',
        'SZL',
        'THB',
        'TJS',
        'TMT',
        'TND',
        'TOP',
        'TRY',
        'TTD',
        'TWD',
        'TZS',
        'UAH',
        'UGX',
        'USD',
        'USN',
        'UYI',
        'UYU',
        'UZS',
        'VEF',
        'VND',
        'VUV',
        'WST',
        'XAF',
        'XAG',
        'XAU',
        'XBA',
        'XBB',
        'XBC',
        'XBD',
        'XCD',
        'XDR',
        'XOF',
        'XPD',
        'XPF',
        'XPT',
        'XSU',
        'XTS',
        'XUA',
        'XXX',
        'YER',
        'ZAR',
        'ZMW',
        'ZWL',
        name='currency',
        create_type=False,
    )
    Currency.create(bind=op.get_bind(), checkfirst=False)

    # merchant

    MerchantCode = pg.ENUM(
        'UNKNOWN',
        'EVIL',
        name='merchant_code',
        create_type=False,
    )
    MerchantCode.create(bind=op.get_bind(), checkfirst=False)

    MerchantOpType = pg.ENUM(
        'UNDERWRITE',
        name='merchant_op_type',
        create_type=False
    )
    MerchantOpType.create(bind=op.get_bind(), checkfirst=False)

    MerchantOpState = pg.ENUM(
        'STAGED',
        'EXECUTING',
        'SUCCEEDED',
        'FAILED',
        'CANCELED',
        name='merchant_op_state',
        create_type=False
    )
    MerchantOpState.create(bind=op.get_bind(), checkfirst=False)

    op.create_table(
        'merchants',
        sa.Column('id', pg.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime, nullable=False, onupdate=sa.func.clock_timestamp(), server_default=sa.text('now()')),
        sa.Column('company_id', pg.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('trace_id', sa.Unicode, index=True),
        sa.Column('name', sa.Unicode, nullable=False),
        sa.Column('phone_number', sa.Unicode, nullable=False),
        sa.Column('tax_id', sa.Unicode, nullable=False),
        sa.Column('country_code', sa.Unicode, nullable=False),
    )

    op.create_table(
        'merchant_ops',
        sa.Column('id', pg.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('_type', MerchantOpType, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('company_id', pg.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('submission_id', pg.UUID, sa.ForeignKey('submissions.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('confirmation_id', pg.UUID, sa.ForeignKey('confirmations.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('settlement_id', pg.UUID, sa.ForeignKey('settlements.id', ondelete='CASCADE'), index=True),
        sa.Column('external_id', sa.Unicode, nullable=False),
        sa.Column('trace_id', sa.Unicode, index=True),
        sa.Column('params', pg.JSON, nullable=False),
        sa.Column('state', MerchantOpState, nullable=False, server_default='STAGED'),
        sa.Column('code', MerchantCode),
        sa.Column('diagnostics', pg.ARRAY(sa.Unicode), nullable=False, server_default=sa.text('array[]::varchar[]')),
    )

    # bank account

    BankAccountCode = pg.ENUM(
        'UNKNOWN',
        name='bank_account_code',
        create_type=False,
    )
    BankAccountCode.create(bind=op.get_bind(), checkfirst=False)

    BankAccountOpType = pg.ENUM(
        'CREDIT',
        'DEBIT',
        'REVERSE_DEBIT',
        name='bank_account_op_type',
        create_type=False
    )
    BankAccountOpType.create(bind=op.get_bind(), checkfirst=False)

    BankAccountOpState = pg.ENUM(
        'STAGED',
        'EXECUTING',
        'SUCCEEDED',
        'FAILED',
        'CANCELED',
        name='bank_account_op_state',
        create_type=False
    )
    BankAccountOpState.create(bind=op.get_bind(), checkfirst=False)

    BankAccountType = pg.ENUM(
        'SAVINGS',
        'CHECKING',
        name='bank_account_type',
        create_type=False
    )
    BankAccountType.create(bind=op.get_bind(), checkfirst=False)

    op.create_table(
        'bank_account_ops',
        sa.Column('id', pg.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('_type', BankAccountOpType, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('company_id', pg.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('submission_id', pg.UUID, sa.ForeignKey('submissions.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('confirmation_id', pg.UUID, sa.ForeignKey('confirmations.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('settlement_id', pg.UUID, sa.ForeignKey('settlements.id', ondelete='CASCADE'), index=True),
        sa.Column('merchant_id', pg.UUID, sa.ForeignKey('merchants.id', ondelete='CASCADE'), index=True),
        sa.Column('external_id', sa.Unicode, nullable=False),
        sa.Column('trace_id', sa.Unicode, index=True),
        sa.Column('reference_id', pg.UUID, sa.ForeignKey('bank_account_ops.id'), index=True),
        sa.Column('account_type', BankAccountType, nullable=False),
        sa.Column('account_number', sa.Unicode, nullable=False),
        sa.Column('bank_code', sa.Unicode, nullable=False),
        sa.Column('country_code', sa.Unicode, nullable=False),
        sa.Column('params', pg.JSON, nullable=False),
        sa.Column('state', BankAccountOpState, nullable=False, server_default='STAGED'),
        sa.Column('code', BankAccountCode),
        sa.Column('diagnostics', pg.ARRAY(sa.Unicode), nullable=False, server_default=sa.text('array[]::varchar[]')),
    )

    # credit card

    CreditCardCode = pg.ENUM(
        'UNKNOWN',
        'DECLINED',
        'LOCKED',
        name='credit_card_code',
        create_type=False,
    )
    CreditCardCode.create(bind=op.get_bind(), checkfirst=False)

    CreditCardVerificationState = pg.ENUM(
        'STAGED',
        'ACCEPTED',
        'REJECTED',
        name='credit_card_verification_state',
        create_type=False
    )
    CreditCardVerificationState.create(bind=op.get_bind(), checkfirst=False)

    op.create_table(
        'credit_card_verifications',
        sa.Column('id', pg.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime, nullable=False, onupdate=sa.func.clock_timestamp(), server_default=sa.text('now()')),
        sa.Column('company_id', pg.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('external_id', sa.Unicode, nullable=False),
        sa.Column('trace_id', sa.Unicode, index=True),
        sa.Column('card_number', sa.Unicode, nullable=False),
        sa.Column('card_security_code', sa.Unicode),
        sa.Column('address', pg.JSON),
        sa.Column('phone_number', sa.Unicode),
        sa.Column('params', pg.JSON, nullable=False),
        sa.Column('state', CreditCardVerificationState, default='STAGED', server_default='STAGED', nullable=False),
        sa.Column('address_matched', sa.Boolean),
        sa.Column('postal_code_matched', sa.Boolean),
        sa.Column('security_code_matched', sa.Boolean),
        sa.Column('code', CreditCardCode),
        sa.Column('diagnostics', pg.ARRAY(sa.Unicode), nullable=False, server_default=sa.text('array[]::varchar[]')),
    )

    CreditCardHoldState = pg.ENUM(
        'STAGED',
        'OPEN',
        'CAPTURED',
        'VOIDED',
        'REJECTED',
        name='credit_card_hold_state',
        create_type=False
    )
    CreditCardHoldState.create(bind=op.get_bind(), checkfirst=False)

    op.create_table(
        'credit_card_holds',
        sa.Column('id', pg.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('company_id', pg.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('merchant_id', pg.UUID, sa.ForeignKey('merchants.id', ondelete='CASCADE'), index=True),
        sa.Column('external_id', sa.Unicode, nullable=False),
        sa.Column('trace_id', sa.Unicode, index=True),
        sa.Column('card_number', sa.Unicode, nullable=False),
        sa.Column('card_security_code', sa.Unicode),
        sa.Column('amount', sa.Integer, nullable=False),
        sa.Column('currency', Currency, nullable=False),
        sa.Column('captured_amount', sa.Integer, nullable=False, server_default='0'),
        sa.Column('params', pg.JSON, nullable=False),
        sa.Column('state', CreditCardHoldState, server_default='STAGED', nullable=False),
        sa.Column('code', CreditCardCode),
        sa.Column('diagnostics', pg.ARRAY(sa.Unicode), nullable=False, server_default=sa.text('array[]::varchar[]')),
    )

    CreditCardOpType = pg.ENUM(
        'CAPTURE_HOLD',
        'VOID_HOLD',
        'REVERSE_HOLD_CAPTURE',
        'CREDIT',
        name='credit_card_op_type',
        create_type=False
    )
    CreditCardOpType.create(bind=op.get_bind(), checkfirst=False)

    CreditCardOpState = pg.ENUM(
        'STAGED',
        'EXECUTING',
        'SUCCEEDED',
        'FAILED',
        'CANCELED',
        name='credit_card_op_state',
        create_type=False
    )
    CreditCardOpState.create(bind=op.get_bind(), checkfirst=False)

    op.create_table(
        'credit_card_ops',
        sa.Column('id', pg.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('_type', CreditCardOpType, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('company_id', pg.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('submission_id', pg.UUID, sa.ForeignKey('submissions.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('confirmation_id', pg.UUID, sa.ForeignKey('confirmations.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('settlement_id', pg.UUID, sa.ForeignKey('settlements.id', ondelete='CASCADE'), index=True),
        sa.Column('external_id', sa.Unicode, nullable=False),
        sa.Column('trace_id', sa.Unicode, index=True),
        sa.Column('hold_id', pg.UUID, sa.ForeignKey('credit_card_holds.id', ondelete='CASCADE'), index=True),
        sa.Column('card_number', sa.Unicode, nullable=False),
        sa.Column('card_security_code', sa.Unicode),
        sa.Column('params', pg.JSON, nullable=False),
        sa.Column('state', CreditCardOpState, nullable=False),
        sa.Column('code', CreditCardCode),
        sa.Column('diagnostics', pg.ARRAY(sa.Unicode), nullable=False, server_default=sa.text('array[]::varchar[]')),
    )


def downgrade():
    # credit card

    op.drop_table('credit_card_ops')

    pg.ENUM(
        name='credit_card_op_type',
        create_type=False
    ).drop(bind=op.get_bind(), checkfirst=False)

    pg.ENUM(
        name='credit_card_op_state',
        create_type=False
    ).drop(bind=op.get_bind(), checkfirst=False)

    op.drop_table('credit_card_holds')

    pg.ENUM(
        name='credit_card_hold_state',
        create_type=False
    ).drop(bind=op.get_bind(), checkfirst=False)


    op.drop_table('credit_card_verifications')

    pg.ENUM(
        name='credit_card_verification_state',
        create_type=False
    ).drop(bind=op.get_bind(), checkfirst=False)

    pg.ENUM(
        name='credit_card_code',
        create_type=False,
    ).drop(bind=op.get_bind(), checkfirst=False)

    # bank account

    op.drop_table('bank_account_ops')

    pg.ENUM(
        name='bank_account_type',
        create_type=False
    ).drop(bind=op.get_bind(), checkfirst=False)

    pg.ENUM(
        name='bank_account_op_type',
        create_type=False
    ).drop(bind=op.get_bind(), checkfirst=False)

    pg.ENUM(
        name='bank_account_op_state',
        create_type=False
    ).drop(bind=op.get_bind(), checkfirst=False)

    pg.ENUM(
        name='bank_account_code',
        create_type=False,
    ).drop(bind=op.get_bind(), checkfirst=False)

    # merchant

    op.drop_table('merchants')

    op.drop_table('merchant_ops')

    pg.ENUM(
        name='merchant_code',
        create_type=False,
    ).drop(bind=op.get_bind(), checkfirst=False)

    pg.ENUM(
        name='merchant_op_type',
        create_type=False
    ).drop(bind=op.get_bind(), checkfirst=False)

    pg.ENUM(
        name='merchant_op_state',
        create_type=False,
    ).drop(bind=op.get_bind(), checkfirst=False)

    # common

    pg.ENUM(
        name='currency',
        create_type=False,
    ).drop(bind=op.get_bind(), checkfirst=False)

    op.drop_table('settlements')

    op.drop_table('submissions')

    op.drop_table('confirmations')

    pg.ENUM(
        name='confirmation_code',
        create_type=False,
    ).drop(bind=op.get_bind(), checkfirst=False)

    pg.ENUM(
        name='instrument_type',
        create_type=False
    ).drop(bind=op.get_bind(), checkfirst=False)

    op.drop_table('passwords')

    op.drop_table('companies')
