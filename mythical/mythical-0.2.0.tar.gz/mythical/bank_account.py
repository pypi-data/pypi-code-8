from . import http, sftp, pilo, Query, QueryIndex, ResourceMixin, Enum, ConfirmationCodes


Codes = Enum([
    'UNKNOWN',
    'DECLINED',
    'LOCKED',
    'MALFORMED',
])

class OpIndex(QueryIndex):

    after = pilo.fields.Datetime(format='iso8601', optional=True)

    before = pilo.fields.Datetime(format='iso8601', optional=True)

    confirmed = pilo.fields.Boolean(optional=True)

    settled = pilo.fields.Boolean(optional=True)

    trace_id = pilo.fields.String(optional=True)


OpStates = Enum([
    'STAGED',
    'EXECUTING',
    'SUCCEEDED',
    'FAILED',
    'CANCELED',
])


OpTypes = Enum([
    'CREDIT',
    'DEBIT',
    'REVERSE_DEBIT',
])

class Op(pilo.Form, ResourceMixin):

    @classmethod
    def query(cls, **filters):
        return Query('/bank_account/ops', Op, OpIndex(filters))

    link = pilo.fields.String()

    id = pilo.fields.String()

    types = OpTypes

    type = pilo.fields.String(choices=OpTypes)

    states = OpStates

    state = pilo.fields.String(choices=OpStates)

    confirmed = pilo.fields.Boolean()

    settled = pilo.fields.Boolean()

    external_id = pilo.fields.String()

    codes = Codes

    code = pilo.fields.String(choices=Codes)

    diagnostics = pilo.fields.List(pilo.fields.String())

    def __call__(self):
        return self.execute()

    def execute(self):
        return self.map(http.put(self.link), reset=True, error='raise')


AccountTypes = Enum([
    'CHECKING',
    'SAVINGS',
])


class OpSubmission(pilo.Form):

    external_id = pilo.fields.String()

    amount = pilo.fields.Integer()

    currency = pilo.fields.String()

    account_number = pilo.fields.String()

    account_type = pilo.fields.String(choices=AccountTypes)

    bank_code = pilo.fields.String(default=None)

    country_code = pilo.fields.String()


class CreditSubmission(OpSubmission):

    pass


class DebitSubmission(OpSubmission):

    pass


class ReverseDebitSubmission(OpSubmission):

    pass


class Submit(pilo.Form):

    external_id = pilo.fields.String()

    # credit

    credit_count = pilo.fields.Integer()

    @credit_count.compute
    def credit_count(self):
        return len(self.credits)

    def credit(self, **kwargs):
        v = CreditSubmission(kwargs)
        self.credits.append(v)
        return v

    credits = pilo.fields.List(
        pilo.fields.SubForm(CreditSubmission), default=list
    )

    # debit

    debit_count = pilo.fields.Integer()

    @debit_count.compute
    def debit_count(self):
        return len(self.debits)

    def debit(self, **kwargs):
        v = DebitSubmission(kwargs)
        self.debits.append(v)
        return v

    debits = pilo.fields.List(
        pilo.fields.SubForm(DebitSubmission), default=list
    )

    # reverse debit

    reverse_debit_count = pilo.fields.Integer()

    @reverse_debit_count.compute
    def reverse_debit_count(self):
        return len(self.reverse_debits)

    def reverse_debit(self, **kwargs):
        v = DebitSubmission(kwargs)
        self.reverse_debits.append(v)
        return v

    reverse_debits = pilo.fields.List(
        pilo.fields.SubForm(ReverseDebitSubmission), default=list
    )

    def __call__(self):
        data = type(self)(self)
        source = http.post(
            '/bank_account/submissions/' + self.external_id, data=data,
        )
        return Submission(source)

    def upload(self):
        data = type(self)(self)
        with sftp.connect():
            return sftp.upload(data.external_id, data, 'bank_account')

    @classmethod
    def download(cls, external_id):
        with sftp.connect():
            src = sftp.download(external_id, 'bank_account/submissions')
        return cls(src)


class Confirmation(pilo.Form):

    link = pilo.fields.String()

    id = pilo.fields.String()

    submission_link = pilo.fields.String()

    submission_id = pilo.fields.String()

    submission_external_id = pilo.fields.String()

    created_at = pilo.fields.Datetime(format='iso8601')

    codes = ConfirmationCodes

    code = pilo.fields.String(choices=ConfirmationCodes)

    diagnostics = pilo.fields.List(pilo.fields.String())


class SubmissionIndex(QueryIndex):

    after = pilo.fields.Datetime(format='iso8601', optional=True)

    before = pilo.fields.Datetime(format='iso8601', optional=True)

    processed = pilo.fields.Boolean(optional=True)

    external_id = pilo.fields.String(optional=True)


class Submission(pilo.Form, ResourceMixin):

    link = pilo.fields.String()

    id = pilo.fields.String()

    external_id = pilo.fields.String()

    created_at = pilo.fields.Datetime(format='iso8601')

    processed = pilo.fields.Boolean()

    confirmation_link = pilo.fields.String()

    tally = pilo.fields.Field()

    ops_link = pilo.fields.String()

    @property
    def ops(self):
        return Query(self.ops_link, Op, OpIndex())

    @classmethod
    def get(self, id):
        return Submission(http.get(
            '/bank_account/submissions/{}'.format(id),
        ))

    @classmethod
    def query(cls, **filters):
        return Query(
            '/bank_account/submissions', Submission, SubmissionIndex(filters),
        )

    def confirmation(self):
        return Confirmation(http.get(self.confirmation_link))

    def process(self):
        return Confirmation(http.post(self.confirmation_link))

    def reset(self):
        http.delete(self.confirmation_link)

    def cancel(self):
        http.delete(self.link)


class Settle(pilo.Form):

    after = pilo.fields.Datetime(format='iso8601', optional=True)

    before = pilo.fields.Datetime(format='iso8601', optional=True)

    trace_id = pilo.fields.String(optional=True)

    type = pilo.fields.String(optional=True)

    limit = pilo.fields.Integer(optional=True)

    def __call__(self):
        params = type(self)(self)
        source = http.post('/bank_account/settlements', params=params)
        return Settlement(source)


class SettlementIndex(QueryIndex):

    after = pilo.fields.Datetime(format='iso8601', optional=True)

    before = pilo.fields.Datetime(format='iso8601', optional=True)


class Settlement(pilo.Form):

    link = pilo.fields.String()

    id = pilo.fields.String()

    created_at = pilo.fields.Datetime(format='iso8601')

    ops_link = pilo.fields.String()

    @property
    def ops(self):
        return Query(self.ops_link, Op, OpIndex())

    @classmethod
    def query(self, **filters):
        return Query(
            '/bank_account/settlements', Settlement, SettlementIndex(filters),
        )
