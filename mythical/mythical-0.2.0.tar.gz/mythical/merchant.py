from . import http, sftp, pilo, Query, QueryIndex, ResourceMixin, Enum


Codes = Enum([
    'UNKNOWN',
    'EVIL',
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
    'UNDERWRITE',
])

class Op(pilo.Form, ResourceMixin):

    @classmethod
    def query(cls, **filters):
        return Query('/merchant/ops', Op, OpIndex(filters))

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


class OpSubmission(pilo.Form):

    external_id = pilo.fields.String()


class UnderwriteSubmission(OpSubmission):

    name = pilo.fields.String()

    phone_number = pilo.fields.String()

    tax_id = pilo.fields.String()

    country_code = pilo.fields.String()


class Submit(pilo.Form):

    external_id = pilo.fields.String()

    # underwrite

    underwrite_count = pilo.fields.Integer()

    @underwrite_count.compute
    def underwrite_count(self):
        return len(self.underwrites)

    def underwrite(self, **kwargs):
        v = UnderwriteSubmission(kwargs)
        self.underwrites.append(v)
        return v

    underwrites = pilo.fields.List(
        pilo.fields.SubForm(UnderwriteSubmission), default=list
    )

    def __call__(self):
        data = type(self)(self)
        source = http.post(
            '/merchant/submissions/' + self.external_id, data=data,
        )
        return Submission(source)

    def upload(self):
        data = type(self)(self)
        with sftp.connect():
            sftp.upload(data.external_id, data, 'merchant')


ConfirmationCodes = Enum([
    'ACCEPTED',
    'MALFORMED',
])


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
            '/merchant/submissions/{}'.format(id),
        ))

    @classmethod
    def query(cls, **filters):
        return Query(
            '/merchant/submissions', Submission, SubmissionIndex(filters),
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
        source = http.post('/merchant/settlements', params=params)
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
            '/merchant/settlements', Settlement, SettlementIndex(filters),
        )
